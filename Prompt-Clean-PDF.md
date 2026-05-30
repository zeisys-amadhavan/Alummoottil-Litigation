# Skewed-PDF → Clean Fair-Copy — Reusable Prompt

Paste the text below at the start of a new conversation, along with the skewed/photographed
PDF you want cleaned up.

---

You are helping me turn a skewed, warped, or photographed PDF into a clean, faithful,
re-typeset "fair copy" PDF. The result should read like a cleaned-up version of the SAME
document — same content, same structure, same line breaks — NOT a redesigned template.
This applies to any document type (court order, letter, recipe, certificate, form, notes,
etc.). Work in the code environment (Python).

## PROCESS

**1. EXTRACT & INSPECT**
- Pull the embedded page images at full resolution (`pdfimages -all`). View them.
- Detect duplicate/re-shot pages: if two pages show the same content, use the CLEAREST
  capture and tell me which pages duplicate. Report the true count of distinct content.

**2. READ THE TEXT FROM THE IMAGES (vision), not raw OCR**
- Transcribe by reading the images directly; use OCR only as a hint. For anything cut
  off, skewed, faint, or blurry, crop that region tightly and rotate a few degrees to
  read it. Zoom into headers, footers, signatures, stamps/seals, and any line sitting
  at a cut edge.

**3. REPRODUCE THE ORIGINAL EXACTLY**
- LINE BREAKS: match where every line breaks in the photo. Draw text line-by-line
  (e.g. `canvas.drawString`), left-aligned / ragged-right — NEVER justified or
  auto-wrapped, unless the original is itself justified.
- VERBATIM wording, including apparent typos and inconsistencies (misspellings, stray
  punctuation, missing spaces, mixed forms like "XI/738" vs "X1/738"). Do not silently
  "correct" anything — preserve the document as-is.
- Match the original pagination (same content on the same page).

**4. MATCH THE LAYOUT POSITIONALLY**
- Reproduce the spatial structure of THIS document, whatever it is: centered headings,
  left-margin labels, indented columns, numbered/bulleted lists, signature blocks,
  right-aligned dates, footers, ingredient lists, etc. Place things where they sit in
  the original and at roughly the original scale, so it looks like the same page.
- Example (a court order): centered header; far-left underlined role labels; a serial-
  number column; party details in a right-hand ragged-right column; bold counsel lines;
  a centered, underlined, letter-spaced "O R D E R"; right-side signature block with
  "(Sd/-)" + name + title (include repeats if the signer signed more than once); bottom-
  left appendix/typed-by lines; a centered stamp line; a bottom-right attestation.
  For other documents, mirror their own equivalent structure instead.

**5. MATCH THE FONT**
- Identify the original typeface by cropping a few words and visually comparing candidate
  fonts (serif vs sans, width, stroke contrast, single- vs double-story 'g', etc.). Pick
  the closest available font. (In this environment, TeX Gyre clones are handy:
  Termes ≈ Times, Schola ≈ Century Schoolbook, Bonum ≈ Bookman, Pagella ≈ Palatino.)
- reportlab can't embed CFF/OTF outlines — convert OTF→TTF first (`otf2ttf`), then register
  regular/bold/italic. Set body size and leading to approximate the original's scale; use
  the correct page size (A4/Letter/etc.).

**6. RECONSTRUCT CUT-OFF CONTENT CAREFULLY**
- Only reconstruct text that's cut off or illegible when you have a sound basis (a parallel
  passage elsewhere in the doc, a known standard format, or a value you can compute/derive).
  Cross-check derived values against other clues in the document. Flag every such reconstruction.

**7. CLARIFY BEFORE FINALIZING**
- Give me a numbered list of everything you are NOT 100% sure of (cut-off text, ambiguous
  digits/letters, uncertain spellings, whether a heading exists, etc.), phrased for quick
  yes/no answers. Wait for my answers, then produce the final PDF.

**8. INTEGRITY SAFEGUARD (conditional)**
- If the document is one that could be mistaken for an authentic original or an official/
  certified instrument (court order, certificate, diploma, ID, signed/stamped legal or
  financial paper), add a small, light-grey italic footer on every page, e.g.:
  "Clean reconstruction transcribed from the original — not a certified copy. Verify
  against the original." Keep it; it must not be passable as the genuine certified item.
- For everyday documents with no such risk (recipes, personal notes, drafts), skip the
  footer.

## DELIVERABLES
- The re-typeset fair-copy PDF (the main deliverable).
- On request, also: a searchable OCR'd cleanup of the original photos, and/or an editable
  Word version.
- Render preview images of each page so I can verify fidelity, then present the final PDF
  for download.
