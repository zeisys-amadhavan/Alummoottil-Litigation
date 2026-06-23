# Document Photo → Clean Page Reconstruction

## Inputs

* `source` — PDF or image
* `page_size` — A4 or Letter
* `output_dpi` — integer (sizes the output canvas only; does not select the processing profile)
* `profile_override` — optional: fast | balanced | detailed (forces a profile; for testing)

## Invariants

These rules hold at every step. Nothing later overrides them.

* No OCR, retyping, redrawing, or regeneration. Every word, number, and punctuation mark in the output is an image crop from the original scan.
* Correction may clean a crop but must never invent letter shapes. If a correction would change a glyph's shape, keep the original crop.
* Glyph distortion must be detected by comparing the corrected crop against the original crop using ink mask, aspect ratio, contour shape, and connected-component structure.
* Illumination normalization is used for analysis only. Final crops are always taken from the original (geometry-corrected) pixels, never from the normalized image, so color and tonal fidelity are preserved.
* Preserve color where present. Non-text elements (logos, stamps, colored signatures, highlights) keep their original color. Text crops keep their original pixels and are placed on a white background; they are only forced toward grayscale/white if global whitening is explicitly applied.
* When segmentation or correction is uncertain, prefer the larger original crop. The escalation order is defined once in the Fallback Rules.
* All placement boxes are axis-aligned rectangles. No diagonal, curved, or polygon placement.
* Background is pure white `#FFFFFF`.
* Every output crop must be traceable to:
  * original rendered-page coordinates
  * corrected-page coordinates
  * final canvas coordinates

## Automatic Processing Profile

The processing profile is not a user input. It is derived deterministically from the **rendered pixel dimensions** (megapixels), which is the single source of truth.

Rationale: pixel count is what segmentation and correction actually depend on, it is one unambiguous number, and it handles image inputs correctly (a photo has its own native resolution, not a derived DPI). For a PDF the render is `2 × output_dpi`, so a higher `output_dpi` monotonically increases rendered pixels and naturally moves the run into a finer profile.

Lower pixel counts reconstruct quickly with coarser segmentation and safer block-level fallbacks. Higher pixel counts may spend more time on finer word-level segmentation and local correction.

### Profile by rendered megapixels

*(Note: Thresholds account for the `2 × output_dpi` render multiplier, where a standard 300 `output_dpi` request yields a ~33 MP render).*

* rendered image `<= 15 MP` → **fast profile**
  * page-level geometry correction
  * line-level grouping
  * word crops only where segmentation is very clear
  * coarse alignment grid
  * minimal per-crop correction
  * prefer line, paragraph, or block crops when uncertain

* rendered image `> 15 MP` and `<= 40 MP` → **balanced profile**
  * page-level and line-level correction
  * word crops where segmentation is stable
  * light per-word correction
  * moderate alignment grid
  * preserve uncertain regions as larger crops

* rendered image `> 40 MP` → **detailed profile**
  * finer connected-component analysis
  * tighter word boxes
  * careful local deskew and affine correction
  * finer alignment grid
  * smaller placement tolerances
  * expect longer processing time

If `profile_override` is set, use it instead of the megapixel-derived profile. Record in the verification summary that an override was applied.

## Pipeline

*(For multi-page inputs, loop through steps 1–12 for each page).*

1. **Render.**
   Rasterize the current page at `2 × output_dpi`.
   Example: 72 DPI output → render at 144 DPI.

2. **Select processing profile.**
   Measure the rendered image size in megapixels and select the profile from the table above. If `profile_override` is set, use it.

3. **Correct page geometry.**
   Detect the page boundary deterministically:
   * threshold
   * edges
   * contours
   * largest quadrilateral

   **Reliable-quadrilateral criteria.** Accept a detected quadrilateral for perspective correction only if it meets all of:
   * exactly 4 vertices after polygon approximation (`approxPolyDP`)
   * internal angles within ~20° of 90°
   * area ≥ 60% of the image
   * after correction, the page aspect ratio (short side / long side) is within 0.60–0.85 in either orientation (covers A4 ≈ 0.707 and Letter ≈ 0.773; the check is applied to the corrected page, not to the warped quad, whose apparent aspect is distorted by perspective)

   Then:
   * reliable quadrilateral → perspective correction
   * skew only → rotation deskew
   * uncertain → keep the rendered image unchanged

4. **Create canvas.**
   Create a pure-white page of `page_size` at `output_dpi`.

5. **Map the usable area.**
   On the corrected page, detect content bounds and margins:
   * left
   * right
   * top
   * bottom

   Map that usable area onto the canvas's usable area. Because content is detected on the render (at `2 × output_dpi`) and placed on the canvas (at `output_dpi`), scale mapped coordinates by `output_dpi / render_dpi` (≈ 0.5). Place content relative to the full canvas only if boundary detection failed.

6. **Normalize illumination (analysis only).**
   Produce a normalized analysis image via adaptive local background estimation to neutralize non-uniform lighting, shadows, and gradients, so connected-component analysis and binarization do not fail in heavily shadowed regions. This image is used only for segmentation/classification measurements. Final crops are taken from the original geometry-corrected pixels (per Invariants), so per-crop contrast normalization is not repeated in Step 9.

7. **Segment.**
   First perform **layout analysis** on the normalized analysis image: detect blocks and columns from rule lines and large whitespace gaps, and establish reading order (handles multi-column pages and fixes paragraph/line ordering before fine segmentation).
   Then segment each block into elements using deterministic methods:
   * connected components
   * projection profiles
   * whitespace gaps
   * line grouping
   * bounding-box merging

   Use the selected processing profile to determine segmentation detail.

8. **Classify.**
   Classify each element by appearance without OCR, using spatial heuristics (aspect ratio, bounding-box dimensions, stroke variance, ink density, local contrast, height consistency):
   * word
   * punctuation/number
   * logo
   * signature/handwriting
   * divider
   * stamp/signatory block
   * hazy text / low-confidence text region
   * uncertain

9. **Correct crops.**
   Crops are cut from the original geometry-corrected pixels. Apply only safe deterministic operations:
   * padding
   * local deskew
   * affine correction
   * mild sharpening
   * mild denoising
   * background whitening (localized)

   Contrast normalization is intentionally omitted here; lighting is handled globally in Step 6 (analysis only) and final crops retain original tone/color.

   Revert to the original crop if the corrected crop distorts glyph shapes, changes connected-component structure too much, or materially changes the ink mask. In the fast profile, avoid expensive per-word correction unless segmentation confidence is high.

10. **Reassemble.**
    Reassemble in detected reading order:
    * paragraph → line → element

    Preserve:
    * approximate x-order
    * spacing
    * line spacing
    * straight horizontal baselines

    Place word crops on straight horizontal baselines aligned to the grid.

    **Grid snapping and collision handling (bounded and deterministic):**
    * an element may shift by at most `snap_tolerance` (profile-dependent; e.g. 0.5× median line height)
    * shifts are **vertical only**; horizontal x-order is never changed
    * elements are never reordered, and lines are never split
    * if a collision cannot be resolved within `snap_tolerance`, do not force placement — escalate that region one level down the Fallback Rules ladder

    Never invent content.

    Keep each special element as one larger crop:
    * logo
    * divider
    * signature
    * handwriting
    * stamp/signatory block
    * hazy text
    * uncertain area

11. **Verify against the corrected source.**
    Check that:
    * content-mask coverage ratio (reconstructed ink ÷ source ink) is within the profile-dependent tolerance
    * no large source region was dropped
    * no large new region was added
    * major blocks are present in corresponding locations
    * baselines are horizontal — per-line baseline deviation ≤ 0.3× median line height
    * x-order, line order, and spacing are preserved
    * no element is clipped at the page edge
    * no unintended overlaps exist
    * all crops are traceable to original rendered-page coordinates, corrected-page coordinates, and final canvas coordinates
    * `page_size`, `output_dpi`, and `#FFFFFF` background are correct

12. **Export.**
    If verification passes, write the PNG at `page_size` and `output_dpi`.
    If verification fails, apply the Fallback Rules and re-verify (see below). The ladder terminates because its last rung — the original rendered page — always passes.

## Fallback Rules

All fallback decisions are deterministic. Per-region fallbacks are applied first, during reassembly. The page-level escalation ladder is only entered if the whole page still fails verification in Step 11.

**Per-region fallbacks** (applied where a specific region fails, not to the whole page):
* boundary detection fails → use full rendered page and keep original margins
* perspective correction uncertain → deskew only
* word segmentation unstable → preserve the affected line, paragraph, or block as one crop
* corrected crop distorts shapes → use the original crop
* placement overlaps, clips, or breaks line order → revert that region to one larger crop
* never force word-level reconstruction when line-level or block-level preservation is safer

**Page-level escalation ladder.** If the page still fails verification after per-region fallbacks, walk down this ladder one rung at a time, re-verifying after each, and stop at the first level that passes. Each rung is strictly less processed (and thus safer) than the one above it, and the final rung always passes, so the procedure is guaranteed to terminate.

1. corrected word crops
2. original word crops
3. line crops
4. paragraph crops
5. block crops
6. corrected full-page crop
7. original rendered page

## Verification Summary

Emit this summary for each run:

* `page_size`
* `output_dpi`
* `render_dpi`
* selected processing profile
* `profile_override` applied (yes/no)
* rendered image size in megapixels
* boundary status
* perspective status
* deskew angle
* content-mask coverage ratio
* max baseline deviation (as fraction of median line height)
* count of word crops
* count of line/block crops
* count of special crops
* count of uncertain crops
* fallback regions used
* fallback ladder level reached
* verification tolerance used
* verification pass/fail
