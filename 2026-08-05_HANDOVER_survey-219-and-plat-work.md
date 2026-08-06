# HANDOVER — Survey 219 register & O.S. 197/1983 plat
**As at 05-08-2026, rev. 2.** Read this first in a new chat. Everything below is already written into the register files.

---

## 1. FILES AND WHAT EACH IS FOR

| File | Contents | Status |
|---|---|---|
| `2026-08-05_Metadata_Survey-219_MASTER-parcel-register.md` | **Rewritten.** 13 tables: master parcel table keyed on Re.Sy. (51 rows), thandapper accounts, the TP 17644 mutation, payment sessions, Malayalam filiations, parent-vs-subdivision arithmetic, groupings, collection queue, provenance, disciplines, and the plat's polygon identification / scale / conventions | **authoritative for parcel data** |
| `2026-01-01_Metadata_Alummoottil-Trust-property.md` | Trust corpus, deeds, buildings, §F plat findings incl. **§F5a the metre finding**, **§G the whole-corpus mutation** | updated |
| `2026-08-05_Metadata_Alummoottil_D2-D4-personal-property.md` | Ramesh Chandran M. (D2) & Jiji Ramesh (D4); **§7.1 the 04-08-2026 session**; 219/26-1 carved out | updated |
| `2026-01-01_Metadata_Alummoottil-personal-property.md` | Trustees, connected persons; **§6.5a D1's own parcel, the Kshema Sabha, and the corrections** | updated |
| `2026-08-05_Metadata_STAGING_ReLIS-219-personal-parcels-and-SRO-deed-screens.md` | Raw extraction log, batches 1–4, with provenance | reference only — batches 5–9 are in the master register |
| `2026-08-05_OS197-1983_FMB_plat_v54.svg` | The plat — four inks, every layer named, 11 callouts | **current** |
| `plat.pdf` | The photocopy of the original sheet | source |

---

## 2. THE SVG — STATE AND CONVENTIONS

**`v54` · XML valid · no duplicate ids, no unnamed groups, no empty groups, zero text overlaps.**

- **Four inks.** **Black** = absolutely certain, traced or read from the original sheet (all 51 dimensions, station geometry, title block). **Blue `#0033aa`** = calculated and believed accurate. **Red `#cc0000`** = unavailable, unidentified or definitely wrong. **Green `#007a33`** = the 31 station corners and the 8 bordering plots N/W/E/S. No shading, no fills.
- **Font ISOCPEUR only**, tracking −50.
- ⚠️ **Adobe PGF.** If re-exported from Illustrator, untick **"Preserve Illustrator Editing Capabilities"** or the embedded snapshot returns and silently reverts every edit — it renders correctly in Safari/Preview but reverts in Illustrator. Suspect this first if edits appear to come back from the dead.
- **Callouts:** 11 quadrilaterals · 11 labels · 11 leaders · 11 dots · 11 arrowheads, one per shape, none shared. Filled dot at the **left or right end of the heading line**; arrowhead at the polygon's **area centroid**.
- **Bordering plots** carry a green rule under the heading and no arrow — they lie outside the plat.
- **Group summaries** (1/6, 5/6, main block, pathway) are groups of shapes, not quadrilaterals: no arrow, found by their green corner string.
- **Bottom panel is red only** — items to be tallied later. Black needs no explanation; blue explanation sits in the label.

### Polygon identification — the state of it
All 11 polygons now carry a parcel and every parcel a polygon, by **corner-letter test first, area second**. Confirmed-by-two-tests: 219/11 (drawn as **two** polygons, union 22.49 vs 21.81), 219/19, 219/27, 219/10, 218/1, 219/28, 219/28-1. **Red, not established:** 219/11-1 (key 5), 219/27-1 (key 8), 219/29 (key 11), and the eastern half of 219/11.

⛔ **At least one of those is wrong** — key 5 draws 3.95 are and 219/29 (0.65) is the only parcel left for it. Resolve against a certified **Ext. C1(a)** or **Bhunaksha**, not against more measurement.

⚠️ The old note "key 9 = 219/11-1, edge signature diff 0.0" is contradicted by the corner-letter test; its reference file was named `219-11.svg`.

---

## 3. FINDINGS TO CARRY FORWARD

**⚠⚠ THE WHOLE CORPUS MUTATED.** All seven parcels — 219/10, 11, 11-1, 19, 27-1, 28-1, 29 — left TP 16961 (five brothers) for a new **TP 17644 in the Trust's own name**, FY 2026-27, **₹504, every one paid 04-08-2026**. **TP 16961 is now empty.** Effected pendente lite; 04-08-2026 is also the date of the D1/D2 day-book production memo in IA 6/2026. The standing finding "mutation to Trust: NOT done" is dead.

**The same session cleared D2's and D4's accounts** — 6872-A ₹432 (219/20, /25, /26) and 17093 ₹38 (219/4). Three accounts, eleven parcels, **₹974** — the identical grouping as 03-06-2023. Payer field not captured on any screen.

**D1 has a personal parcel in survey 219** — 219/9-2, 3.05 are, TP 17245, `Late T K Madhava Panicker മകൻ`, paid 26-01-2026.

**The Kshema Sabha is a landholder** — 219/9-3, 14.57 are, TP 16111, President + Secretary. It is the Trust plot's recited eastern boundary.

**219/26 subdivided** — 219/26-1, 1.82 are, TP 17246, Shantha wife of Chandran; TP adjacent to D1's 17245, same PIN. Nothing inferred.

**The plat's dimensions are in METRES, not feet** — established twice over. The sheet converts are→cent at **2.4710**. Derived: 13/15 conveyed = **25.497 are**; 35.30 − 0.49 + 3.25 = **38.06 are**, equal to TP 16961 on the receipt; Chellamma's residue **1.39 are**, equal to TP 6874-A. Every block on the sheet closes to the digit.

**219/28-1 is 2.10, not 2.01** — the revenue record confirms the plat against the O.S. 243/2024 schedule.

**219/23 was wrong for two years** — ഭാര്യ, wife of Philip, not son. **219/14 changed holder and extent** — 0.48 / Rakesh S., not 2.03 / Seethalakshmi.

**Carried forward unchanged:** Deed 299/I/2024 conveyed only 13/15 · the 1/6 sharers and the 1482/2021 gift · the plot-letter conflict · the 2007 Trust Deed's internal contradiction · 219/25 and /26 carry PokkuVaravu, so a mutation instrument exists.

---

## 4. STANDING DISCIPLINE

- **CENT = ARE × 2.4711** in this register; **the plat uses 2.4710**. Immaterial at these extents; it explains third-decimal differences.
- **The plat's dimensions are metres.** Read as feet, every parcel comes out ten times too small.
- **Never read a relationship off the English label in a Land Record screen.** 219/23 is the proved instance. Word order can also be wrong — 219/18-3 inverts name and parent.
- **BTR vs PokkuVaravu describes the register entry, not the acquisition date.**
- **Thandapper numbers are not a chronology** — 6871 / 6872-A / 6874-A are three adjacent numbers across three unrelated holders.
- **Never sum a parent with its own sub-parcels** — 219/9, /13, /18 and /26 all print their full extent alongside sub-parcels.
- **Four Channatty filiations are stated; only Saradamani reaches Chellamma.** Prove the tree from the 1956 Book-3 will, the 1958 Book-1 deed and the O.S. 197/1983 record.
- **Kesavan Channar's line is not the five brothers.** Do not merge.
- **The portal payer field** evidences whose account effected payment, not whose money it was.
- Everything held is a **screen capture**; the only government-issued item is receipt **KL04040204922/2023**, and that is a photocopy.
- **Record register changes as facts and characterise nothing.** The mutation file states who applied and on what instrument.

---

## 5. IMMEDIATE NEXT PULLS

1. **Village Office mutation file / ReLIS Pokkuvaravu for TP 17644** — applicant, date, instrument, whether one application covered all seven. **Top of the list.**
2. **Receipt / GRN for the 04-08-2026 session** — the payer field across all three accounts.
3. **Village Office mutation files** — TP 6872-A (219/25, /26) · TP 17245 (D1's 219/9-2) · TP 17246 (219/26-1) · TP 12732 (Lisy Reji Varghese).
4. **Village Office register** — the four non-reducing parents (219/9, /13, /18, /26); the 219/18-3 inversion; 219/14 Seethalakshmi → Rakesh S.
5. **Bhunaksha**, Block 013 survey 219 — parcel shapes, to settle keys 5, 8, 11 and the eastern half of 219/11.
6. **Certified Ext. C1(a)** — the plot-letter conflict and the polygon identification.
7. **A 600 dpi scan of the plat block.** The photocopy PDF holds one raster of 901 × 1418 px for the whole sheet; the drawn block is 324 × 327 px. The annotation inside 219/11 and 219/19 cannot be recovered from this file.
8. Unpulled sub-divisions implied by the numbering: 219/1-3 · 13-3 · 14-4 · 16-1 · 17-1 · 18-1 · 18-2.
9. **ReLIS Land Record** on every parcel new in batches 6–9 — the BTR/PokkuVaravu remark, which Tax Dues does not carry.

**Tip:** crop ReLIS screenshots to the results table — the left search panel is identical every time and wastes about half the image. 8–10 per message.
