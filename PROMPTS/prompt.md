# PROMPT — Scanned Document → Clean Typed Twin (reusable)

I will upload scanned or photographed pages of typed documents, one or more at a time, and tell you the font (default: Times New Roman — if unavailable, use Liberation Serif, its metric twin, so layout is identical). Recreate each document as a clean, selectable-text PDF "twin" of the original.

## Fidelity rules (absolute — breaking these makes the PDF useless)

1. Transcribe character by character, exactly as typed. Preserve ALL typos, spelling variants, odd punctuation, stray spaces, capitalization quirks, grammatical errors, unclosed quotes, and internal inconsistencies. Never correct, normalize, or improve anything, and never reposition content.
2. Preserve the original's line breaks exactly — the same words on the same lines.
3. Preserve layout logic: indents, hanging indents, centered headings, justification (re-justify justified lines between the measured margins; leave paragraph-final ragged lines ragged), true superscripts (1st, 2nd, 16th…), bold, italics, underlines.
4. Reproduce structural quirks too: mixed paragraph spacing, an oddly indented item, an off-center element — if the original does it, the twin does it.
5. Omit only what is not typed content: handwritten signatures, "True Copy" endorsements, stamps, and scan noise (specks, smudges, binding shadows, edge strips). List every omission in your report.
6. Never add content the scan does not show (e.g. do not invent a missing page number) — flag it instead.

## Geometry rules (the only changes allowed)

- Idealize the grid: deskew; perfectly straight baselines; uniform leading within each block; uniform margins; no tilt, warp, or perspective distortion.
- Measure everything from the scan — line bands, margins, leading, block gaps, centers, and font sizes (fit sizes by matching known text widths). Do not assume standard values.
- Keep the text block where the scan places it on the page; do not re-center unless asked.
- For page 2+ of a document whose page-1 grid is established, reuse the page-1 grid for consistency, anchoring vertical positions to each page's own measurements. If a photo is too warped to trust its frame, fall back to the established grid and say so.
- Match the source page size (e.g. A4).

## Verification (required before building)

- Cross-check the transcription with at least two independent reads (your own reading of the image plus OCR). Investigate every disagreement at pixel level where possible: stroke heights for i vs l, below-baseline tail for comma vs period, template correlation for ambiguous vowels, gap measurement for missing spaces.
- If two scans supposedly contain the same text, diff them line by line — never assume identity; report every confirmed difference.
- Where the scan genuinely cannot resolve a character, choose the typographically/grammatically standard reading and FLAG it explicitly for my confirmation. Never silently guess; my reading of the paper original overrides pixel analysis.
- Standing conventions (keep unless I say otherwise): typographic curly quotes and apostrophes (" " ') since the documents are Word-produced; lowercase "is / its / in" where capital-I and lowercase-i are pixel-identical (flag once); preserve unbalanced quotes as-is.

## Deliverables per document

1. The recreation PDF — selectable text, embedded fonts, superscripts as genuinely raised smaller text, italics/bold as real font variants, sensible PDF title metadata.
2. A side-by-side proof sheet PNG (scan | recreation, one row per page).
3. A short report: idealizations applied, quirks deliberately preserved, omissions, and every flagged uncertain reading.

## QA before delivery

- Extract the recreation's text layer and diff it against the transcription.
- Detect the recreation's line bands and compare positions with the deskewed scan (expect agreement within a few points; explain intentional deviations).
- Verify every justified line fits its measured slot with plausible word spacing.
- Fix anything found, rebuild, re-verify. Only then deliver.
