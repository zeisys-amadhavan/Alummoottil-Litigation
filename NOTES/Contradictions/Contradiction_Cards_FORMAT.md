# Contradiction Matrix — Card PDF Format Specification

This document fully describes the one‑card‑per‑page PDF format used for the
Contradiction Matrix (O.S. 214/2025). Hand this file plus an updated matrix
(spreadsheet or list) to recreate an identical-looking PDF.

The governing design principle is a **fixed grid**: every element sits at the
**same coordinates and the same size on every page**. Content never moves or
resizes a box — instead the text is auto‑sized as large as possible to fill the
fixed box it lives in.

---

## 1. Input data

Each contradiction is one record with eight fields. Column names from the
source spreadsheet map to the keys used by the generator:

| Spreadsheet column | Generator key | Goes into |
|---|---|---|
| `#`            | `n`     | Number badge (top‑left) |
| `ISSUE`        | `issue` | Heading (top‑right) |
| `RECORD A`     | `a`     | Left card body |
| `RECORD B`     | `b`     | Right card body |
| `CONFLICT`     | `c`     | Conflict box |
| `SIGNIFICANCE` | `s`     | Significance box |
| `SEVERITY`     | `sev`   | (metadata; not drawn on the card) |
| `TYPE`         | `typ`   | (metadata; not drawn on the card) |

The generator reads a Python list named `DATA` (see §7). To rebuild from the
spreadsheet, read the sheet `Credibility_Matrix_Ramesh_Chand` and build that
list, one dict per row.

### Writing conventions (must be preserved)
- **One consistent label per actor**, never mixed: `Plaintiff` = Anoop;
  `D1` = the Trust; `D2` = Ramesh Chandran (Managing Trustee); `D3` = Sivadasan;
  `D4` = Jiji Ramesh; `D5` = Arun B. Unni; `D6` = V. Nandakumar; `D7` = B. Nadarajan.
  In narration use the label (e.g. "D2's plaint", not "his plaint" / "Ramesh Chandran").
- **Quotations from the court record are verbatim** — never paraphrase text inside
  `"..."`. Only the connective narration may use the consistent labels.
- **Conflict** states the clash between Record A and Record B.
  **Significance** states a *distinct* "so what" (the legal/evidential consequence) —
  it should not merely restate the Conflict.
- Flag unverified items in the text itself (e.g. `[evidence pending]`,
  `[to be verified]`).

---

## 2. Page & grid geometry (the fixed template)

- Page size: **A4 portrait** (210 × 297 mm).
- All measurements in millimetres; origin is bottom‑left (ReportLab convention).
- `PW = 210mm`, `PH = 297mm`, `top = PH − M`, `usable = PW − 2·M`.

| Constant | Value | Meaning |
|---|---|---|
| `M`       | 9 mm    | Page margin (all sides) |
| `R`       | 4.0 mm  | Corner radius (all rounded rects) |
| `BORDER`  | 1.4 pt  | Box outline weight |
| `PAD`     | 4.5 mm  | Inner text padding in every box |
| `BADGE`   | 32 mm   | Number badge — square, top‑left |
| `BAND_H`  | 38 mm   | Header band height (badge + heading) |
| `GAP`     | 4 mm    | Vertical gap between stacked blocks |
| `COLGAP`  | 6 mm    | Gap between Record A and Record B |
| `COLW`    | (usable − COLGAP)/2 | Width of each record card |
| `REC_H`   | 136 mm  | Record card height (both cards) |
| `RECHDR_H`| 14 mm   | Black header bar height on each record card |
| `CON_H`   | 42 mm   | Conflict box height |
| `SIG_H`   | 48 mm   | Significance box height |

**Vertical stack (top → bottom), fixed on every page:**

```
top (=288mm)
 ├─ Header band ............ BAND_H (38mm)   badge left, heading right
 │     BAND_BOT = top − BAND_H
 ├─ GAP (4mm)
 ├─ RECORD A | RECORD B .... REC_H (136mm)   two columns, COLGAP between
 │     REC_TOP = BAND_BOT − GAP ;  REC_BOT = REC_TOP − REC_H
 ├─ GAP (4mm)
 ├─ CONFLICT box ........... CON_H (42mm)    full width
 │     CON_TOP = REC_BOT − GAP ;  CON_BOT = CON_TOP − CON_H
 ├─ GAP (4mm)
 └─ SIGNIFICANCE box ....... SIG_H (48mm)    full width
       SIG_TOP = CON_BOT − GAP
```

This consumes ≈ 285 mm of the 297 mm height, leaving ~12 mm bottom margin.

---

## 3. Typography

Two type families. The real target fonts are proprietary; the substitutes below
are what the generator uses.

| Role | Target font | Substitute used | Notes |
|---|---|---|---|
| Body + heading | **Cambria** | **Caladea** | Caladea is *metrically identical* to Cambria — visually equivalent. |
| Conflict/Significance label (bold) | Cambria Bold | Caladea Bold | Registered as the bold of the `Cambria` family. |
| Number + RECORD A/B labels | **Helvetica Neue Condensed Bold** | **Barlow Semi Condensed Bold** | Close neo‑grotesque match, slightly less tight. |

Font file locations / sources:
- Caladea (regular + bold): system, `/usr/share/fonts/truetype/crosextra/Caladea-Regular.ttf`
  and `Caladea-Bold.ttf` (package `fonts-crosextra-caladea`).
- Barlow Semi Condensed Bold: download
  `https://raw.githubusercontent.com/google/fonts/main/ofl/barlowsemicondensed/BarlowSemiCondensed-Bold.ttf`.

To use the **exact** fonts instead, drop in `Cambria.ttf` / `Cambriab.ttf` and
`HelveticaNeue-CondensedBold` and point the three `registerFont` calls at them.
Nothing else changes.

### Sizing rules
- **Body text**: one size per page, chosen as the **largest size in the range
  [10.5 pt … 22 pt]** at which *all four* boxes (Record A, Record B, Conflict,
  Significance) still fit inside their fixed inner areas. This is why a light
  page renders ~20 pt and a dense page ~16 pt while the boxes stay identical.
  Leading = `1.30 × size`.
- **Heading** (`issue`): auto‑fit, start 30 pt, step down by 0.5 to min 15 pt,
  until it fits the heading width and `BAND_H`. Leading = `1.13 × size`.
- **Number badge**: auto‑fit, start 66 pt, shrink until the digits fit
  `BADGE − 9mm` wide. Vertically optically centred.
- **RECORD A / RECORD B labels**: auto‑fit, start 24 pt, shrink to fit
  `COLW − 9mm`.

### Alignment
- Body text (records, conflict, significance): **left‑aligned (ragged right)** —
  chosen over justified because it reads better on narrow columns / small screens.
- Heading: left‑aligned, top‑aligned within the band.
- Number and RECORD labels: centred (white on black).
- All box body text is **top‑aligned** inside its box (short content leaves
  whitespace at the bottom of the box — this is intentional).

---

## 4. Colours

| Element | Fill | Text |
|---|---|---|
| Number badge | Black `#000000` | White |
| RECORD A header bar | Black | White |
| RECORD B header bar | Black | White |
| Record A body | White `#FFFFFF` | Black |
| **Record B body** | **Light grey `#F2F2F2`** | Black |
| Conflict box | White | Black (label bold) |
| Significance box | White | Black (label bold) |
| All borders | Black `#000000`, 1.4 pt | — |

The light grey on Record B is an **orientation cue only** (instantly signals the
A/B split); it is kept at ~5% so black text on it stays far above accessibility
contrast thresholds. Significance is intentionally **not** shaded.

---

## 5. Per‑element drawing notes

- **Record card**: draw the white/grey rounded body rect first (with black
  border), then overlay the black header bar. The header bar is a rounded rect
  whose **bottom corners are squared off** by painting a plain rect of height
  `R` across its lower edge — giving rounded top corners, flat bottom.
- **Conflict / Significance**: single rounded rect, no header bar. The label is
  inline: `**CONFLICT:** <text>` / `**SIGNIFICANCE:** <text>` (bold label, then
  regular body, same paragraph).
- No footer or page number on the card pages (matches the template).

---

## 6. Optional legend page

A "Key" page may be prepended as page 1 (cast = Plaintiff/D1–D7, suits &
proceedings, key instruments, and the note that labels are consistent and quotes
verbatim). It is a plain reference page, not a card. Optional — omit if not wanted.

---

## 7. Generator script (canonical, reproducible)

Save the matrix as a module `data_mod.py` containing:

```python
# data_mod.py
DATA = [
  dict(n=1, sev="Major", typ="Misrepresentation",
       issue="…", a="…", b="…", c="…", s="…"),
  # … one dict per contradiction, in order …
]
```

Then run the generator below. It encodes every constant from §2–§5.

```python
# gen.py  — build the contradiction-card PDF
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from xml.sax.saxutils import escape
from importlib.machinery import SourceFileLoader

# ---- fonts (swap paths here for exact Cambria / Helvetica Neue Condensed) ----
pdfmetrics.registerFont(TTFont('Cambria',    '/usr/share/fonts/truetype/crosextra/Caladea-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Cambria-Bd', '/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Cond',       'BarlowSemiCondensed-Bold.ttf'))
pdfmetrics.registerFontFamily('Cambria', normal='Cambria', bold='Cambria-Bd')

BLACK, WHITE = colors.black, colors.white
GREYB = colors.HexColor('#F2F2F2')        # Record B orientation tint
PW, PH = A4

# ---- fixed grid ----
M, R, BORDER, PAD = 9*mm, 4.0*mm, 1.4, 4.5*mm
top, usable = PH - M, PW - 2*M
BADGE, BAND_H = 32*mm, 38*mm
BAND_BOT = top - BAND_H
GAP, COLGAP = 4*mm, 6*mm
COLW = (usable - COLGAP)/2
REC_TOP, REC_H, RECHDR_H = BAND_BOT - GAP, 136*mm, 14*mm
REC_BOT = REC_TOP - REC_H
CON_TOP, CON_H = REC_BOT - GAP, 42*mm
CON_BOT = CON_TOP - CON_H
SIG_TOP, SIG_H = CON_BOT - GAP, 48*mm
CAP, FLOOR = 22.0, 10.5

DATA = SourceFileLoader('m', 'data_mod.py').load_module().DATA

def para(text, font, size, lead, align=TA_LEFT, color=BLACK):
    return Paragraph(text, ParagraphStyle('s', fontName=font, fontSize=size,
                     leading=lead, alignment=align, textColor=color))
def esc(t): return escape(str(t)).replace('\n', '<br/>')

def fits(text, w, h, fs, prefix=None):
    body = f'<b>{prefix}</b> {esc(text)}' if prefix else esc(text)
    _, ht = para(body, 'Cambria', fs, fs*1.30).wrap(w, 1e6)
    return ht <= h

def page_font(d):
    rw, rh = COLW-2*PAD, REC_H-RECHDR_H-2*PAD
    cw = usable-2*PAD
    fs = CAP
    while fs >= FLOOR:
        if (fits(d['a'], rw, rh, fs) and fits(d['b'], rw, rh, fs) and
            fits(d['c'], cw, CON_H-2*PAD, fs, 'CONFLICT:') and
            fits(d['s'], cw, SIG_H-2*PAD, fs, 'SIGNIFICANCE:')):
            return fs
        fs -= 0.25
    return FLOOR

def draw_number(c, n):
    c.setFillColor(BLACK); c.roundRect(M, top-BADGE, BADGE, BADGE, R, 0, 1)
    ns = 66
    while ns > 20 and pdfmetrics.stringWidth(str(n), 'Cond', ns) > BADGE-9*mm: ns -= 1
    c.setFillColor(WHITE); c.setFont('Cond', ns)
    asc = pdfmetrics.getAscent('Cond')/1000*ns
    c.drawCentredString(M+BADGE/2, top-BADGE/2 - asc*0.36, str(n))

def draw_heading(c, issue):
    hx = M+BADGE+6*mm; hw = PW-M-hx; hs = 30
    while hs >= 15:
        hp = para(esc(issue), 'Cambria', hs, hs*1.13); _, hh = hp.wrap(hw, 1e6)
        if hh <= BAND_H: break
        hs -= 0.5
    hp.drawOn(c, hx, top-hh)

def record_card(c, x, label, text, fs, bg=WHITE):
    c.setFillColor(bg); c.setStrokeColor(BLACK); c.setLineWidth(BORDER)
    c.roundRect(x, REC_BOT, COLW, REC_H, R, 1, 1)
    c.setFillColor(BLACK)
    c.roundRect(x, REC_TOP-RECHDR_H, COLW, RECHDR_H, R, 0, 1)
    c.rect(x, REC_TOP-RECHDR_H, COLW, R+0.3*mm, 0, 1)          # square the bar's bottom
    ls = 24
    while ls > 12 and pdfmetrics.stringWidth(label, 'Cond', ls) > COLW-9*mm: ls -= 1
    c.setFillColor(WHITE); c.setFont('Cond', ls)
    asc = pdfmetrics.getAscent('Cond')/1000*ls
    c.drawCentredString(x+COLW/2, REC_TOP-RECHDR_H/2 - asc*0.36, label)
    p = para(esc(text), 'Cambria', fs, fs*1.30); _, h = p.wrap(COLW-2*PAD, 1e6)
    p.drawOn(c, x+PAD, REC_TOP-RECHDR_H-PAD-h)

def full_box(c, y_top, box_h, prefix, text, fs):
    c.setFillColor(WHITE); c.setStrokeColor(BLACK); c.setLineWidth(BORDER)
    c.roundRect(M, y_top-box_h, usable, box_h, R, 1, 1)
    p = para(f'<b>{prefix}</b> {esc(text)}', 'Cambria', fs, fs*1.30)
    _, h = p.wrap(usable-2*PAD, 1e6)
    p.drawOn(c, M+PAD, y_top-PAD-h)

c = canvas.Canvas('Contradiction_Matrix_cards.pdf', pagesize=A4)
c.setTitle('Contradiction Matrix')
for d in DATA:
    fs = page_font(d)
    draw_number(c, d['n'])
    draw_heading(c, d['issue'])
    record_card(c, M, 'RECORD A', d['a'], fs)
    record_card(c, M+COLW+COLGAP, 'RECORD B', d['b'], fs, bg=GREYB)
    full_box(c, CON_TOP, CON_H, 'CONFLICT:', d['c'], fs)
    full_box(c, SIG_TOP, SIG_H, 'SIGNIFICANCE:', d['s'], fs)
    if fs <= FLOOR + 0.01:
        print(f"WARN #{d['n']} hit the floor font — its box may be overfull")
    c.showPage()
c.save()
```

---

## 8. How to regenerate (quick recipe)

1. Update the matrix (spreadsheet rows or the `DATA` list).
2. Ensure the three font files are available (Caladea on system; download Barlow
   Semi Condensed Bold; or substitute the exact fonts).
3. Build `data_mod.py` from the matrix (one `dict` per row, keys
   `n, issue, a, b, c, s, sev, typ`).
4. Run `gen.py`. Output: `Contradiction_Matrix_cards.pdf`.
5. If any `WARN … hit the floor font` prints, that row's content is too long for
   its fixed box even at 10.5 pt — shorten the text, or (last resort) raise the
   relevant box height in §2, which then applies to **all** pages.

---

## 9. Tunable knobs (change deliberately, they affect every page)

- Make text larger overall → raise `CAP` (but light pages may then look oversized).
- Give records more room → raise `REC_H` and reduce `CON_H` / `SIG_H` to match.
- Tighter/looser cards → change `R`, `BORDER`, `PAD`, `GAP`, `COLGAP`.
- Different Record B tint → change `GREYB` (keep it ≤ ~8% so contrast holds).
- Justified body instead of ragged → set `align=TA_JUSTIFY` in `para()` defaults
  (not recommended for the narrow columns).
```
