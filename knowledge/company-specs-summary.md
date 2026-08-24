# Company Product Specifications — Summary

Extracted from `GDS_spec/시방서.zip` (company 특별시방서 = special/product specifications), the
authoritative source for product-specific requirements. This file summarizes them for quick
agent reference; **the original PDFs are the legal source of truth** — re-read them directly for
any figure that will be quoted in a contractual or safety-critical document.

Source PDFs (Korean, extracted to `knowledge/시방서/` is NOT how they're stored — they live
zipped in `GDS_spec/시방서.zip`; extract with `python3 -c "import zipfile;
zipfile.ZipFile('GDS_spec/시방서.zip').extractall('<destdir>')"` run from the repo root, or ask
the site engineer for a fresh extraction if the temp copy is gone):

1. 페블테크 시방서 - H.pdf
2. 하이셀 시방서 0811.pdf
3. 조립골재 시방서 - H.pdf
4. 구속셀 시방서0730.pdf
5. 메가헬리컬파일 특기시방서(114-7.5t)_20260720.pdf
6. 메가헬리컬파일 특기시방서(114-9t)_20260720.pdf

## ✔ Headline finding: this is the PRD's primary application's own design method

All four aggregate-replacement products below (페블테크, 하이셀, 조립골재, 구속셀) are governed
by **KCS 11 30 10 (연약지반 치환공, soft-ground replacement) and MOLIT 구조물기초설계기준
Ch.4 (얕은기초, shallow foundations)** — i.e. they are **soft-ground *foundation replacement/
improvement* methods**, used for the PRD's **primary application (§4.2a): permanent building
foundation support**. This is not a literal implementation of BR470's tracked-plant
working-platform LSF/punching-shear equation — that method (§4.2b) applies to the PRD's
*additional* application (temporary tracked-plant platforms) specifically. See
`knowledge/aggregate-working-platform-prd.md` §4.2 for both methods side by side.

- **Bearing capacity:** computed by Terzaghi + Meyerhof + an empirical formula (페블테크,
  조립골재), with the **lowest of the three governing**; 하이셀 and 구속셀 specs use
  **Meyerhof only**. Reference: 구조물기초설계기준해설 (2009), pp.186/191/216.
- **Settlement:** Schmertmann method + elastic theory, **larger of the two governing**.
- Platform thickness is iterated until both the bearing-capacity and settlement checks pass —
  there is no explicit "LSF ratio" computed or reported in these company documents.

**Practical guidance for the design agent:** first confirm which application governs (PRD §1 —
primary/building vs. additional/temporary tracked-plant). For the primary (building foundation)
application — the ordinary case, and what every real project design/review package on file
actually is — lead with the MOLIT Terzaghi/Meyerhof/empirical + Schmertmann/elastic method (this
is what the company's own 검토서/계산서 will show — see `design-worked-examples.md`). Use the
PRD's BR470 LSF method (§4.2b) only when the question is specifically about a temporary
tracked-plant working platform. The two frameworks are not interchangeable — say explicitly which
one applies so nobody expects an LSF ratio out of a building-foundation calc, or a FS=3.0
bearing-capacity check out of a temporary-platform calc.

## 페블테크 (Pebble-Tech) — aggregate-only platform

Patented product, KR 10-2688653. Scope: soft-ground replacement using graded/blended aggregate,
no geosynthetic.

- **Standards:** KCS 11 30 10:2021; KS F 2444 (평판재하시험, plate load test); KS F 2502
  (체가름시험, sieve analysis); KS F 2511 (0.08mm체 통과량, fines content).
- **Bearing method:** Terzaghi / Meyerhof / empirical — lowest governs.
- **Settlement method:** Schmertmann / elastic theory — larger governs.
- **Aggregate grading (hard spec — more precise than PRD's generic "Type 1 equivalent"):**
  - Max particle size ≤ 100 mm
  - Fines fraction < 5 mm ≤ 15%
  - Sand/silt fraction < 2 mm ≤ 5%
  - Particle-size ratio Dmax/D80 ≥ 3
  - Coefficient of curvature Cg: 0.7–1.3
  - Coefficient of uniformity Cu: 1.7–5
- **Optional geotextile mat:** design tensile strength ≥ 50 kN/m.
- **Lift thickness:** ≤ 300 mm per compacted layer (hard ceiling; PRD's 150–300mm "loose" range
  is a reasonable working assumption for achieving this, but the spec's compliance figure is
  the 300mm max).
- **QC — plate load test (KS F 2444):** minimum 1 test after completion; test location "by
  agreement with the supervising engineer" — looser than the PRD's 1-per-200–500m² grid.
  Present the PRD grid frequency as the general recommendation, but confirm actual required
  frequency against the specific project's approved ITP.

## 하이셀 (Hi-Cell) — geocell-reinforced platform

**Important product-identity clarification:** 하이셀 is a **geocell (지오셀)**, i.e. a 3D
honeycomb HDPE cell structure filled with confined aggregate — not a flat geogrid/geotextile.
The PRD's Giroud–Han (geogrid) framing is a reasonable *international* design-method analogue,
but the company's own bearing calc for this product does not literally run Giroud-Han geogrid
theory.

- **Standard:** KCS 11 30 10:2025 (note: newer revision date than 페블테크's 2021 reference).
- **Extra required input:** 지하안전평가보고서 (underground safety assessment report) required
  if excavation depth ≥ 10 m.
- **Bearing method:** Meyerhof only.
- **Geocell hard specs:**
  - Cell height: 200–300 mm
  - HDPE sheet thickness: ~1.2 mm (perforated for lateral drainage, embossed for fill bonding)
  - Cell internal diameter: ~300 mm
  - Anchoring: 13 mm deformed rebar stake pins
  - Panel-to-panel joints: geocell key (H-shaped clip), or wire/cable ties as a substitute
- **Aggregate grading:** same envelope as 페블테크 (100mm max, ≤15% fines <5mm, ≤5% <2mm,
  Dmax/D80≥3, Cg 0.7–1.3, Cu 1.7–5).
- **Installation sequence:**
  1. Place anchor pins at the leading edge, spaced at the cell diameter.
  2. Unroll cells in the direction of work.
  3. Check alignment by string line / visual check.
  4. Pin the cell interior to prevent distortion during fill placement.
  5. Key-lock (or wire-tie) panel overlaps.
- **Site-specific rule:** at a soil/weathered-rock interface, over-excavate the weathered rock an
  additional 3–4 m before installing 하이셀ㅡ this materially affects excavation depth/program
  planning wherever rockhead is encountered within the platform zone.
- **QC:** plate load test, same as 페블테크 (min. 1 test, location by agreement).

## 조립골재 (Assembled/Graded Aggregate)

Effectively a generic/unbranded variant of the same aggregate-replacement product line as
페블테크: same KCS/KS references, same grading envelope, same 300mm lift cap, same plate-load
QC. **Difference:** bearing method is Meyerhof only (not the Terzaghi/Meyerhof/empirical triad
used for 페블테크) — closer to 하이셀's calc basis than 페블테크's.

## 구속셀 (Confinement Cell)

Near-identical to 하이셀, same installation sequence and 3–4m weathered-rock over-excavation
rule, same Meyerhof-only bearing method. **Product difference:** HDPE sheet is **1.6 mm thick**
(vs. 하이셀's 1.2 mm) — i.e. 구속셀 is the heavier-duty geocell tier of the same product family.
Same cell height (200–300mm), internal diameter (~300mm), 13mm rebar pins, key/wire-tie joints.

> Note: this document's Korean text had OCR/encoding corruption on several pages; the numeric
> specs above were cross-checked against the parallel-structured 하이셀 spec and the legible
> portions of 구속셀's own text. Re-verify against the source PDF before quoting in a formal
> deliverable.

## 메가헬리컬파일 (Mega Helical Pile) — 7.5t and 9t variants

**Different system, same reference set.** This is a self-driving helical steel pipe pile with
cement grouting, used for *permanent/deep* foundations — not a working-platform product. Likely
present because the same projects use it as a deep-foundation alternative adjacent to or beneath
the temporary platform. Included here for cross-domain awareness; a "design" or "construction"
agent should flag when a question is actually about this system rather than the aggregate
working platform.

- **Design capacity:** Meyerhof-based empirical formula —
  `Qu = 30·Ne·Ap + U·Σ(fs·Li)`, where Ne = SPT N-value at tip, Ap = grout cross-section area,
  U = grout perimeter, fs = 0.5·Nc (cohesive) + 0.2·Ns (granular). Governing capacity =
  min(steel material capacity, soil capacity).
- **Settlement limit:** total settlement < 25 mm = pass; ≥25mm = N.G., iterate design.
- **Steel:** P110 grade, yield strength ≥ 758 MPa; 114.3 mm OD; wall rated 7.5t or 9.0t variant;
  base plate 300×300×20mm; M16 high-strength bolted splice connections.
- **Grouting:** cement 871 kg/m³, water 723 kg/m³ (W/C ≈ 83%), OPC per KS L 5201; admixture
  chlorides/sulfates/nitrates each < 0.1%.
- **Installation tolerance:** verticality/inclination ≤ 1/50; plan position deviation ≤
  max(D/4, 100mm) from design location; final penetration criterion = < 5mm advance per 20 motor
  rotations.
- **Load testing:** static load test at ≥ 2× design load; dynamic (PDA) test per ASTM D4945;
  test frequency ≥ 1% of total piles (minimum 1 pile even if fewer than 100 total); material
  test certificate every 1000 piles or per site.

## Quick-reference table — aggregate-replacement product family

| Product | Type | Sheet/mat spec | Bearing method | Standard |
|---|---|---|---|---|
| 페블테크 | Aggregate only | Optional geotextile mat ≥50 kN/m | Terzaghi/Meyerhof/empirical (lowest governs) | KCS 11 30 10:2021 |
| 조립골재 | Aggregate only (generic) | — | Meyerhof only | KCS 11 30 10 |
| 하이셀 | Geocell + aggregate | HDPE 1.2mm, cell H 200–300mm, ⌀~300mm | Meyerhof only | KCS 11 30 10:2025 |
| 구속셀 | Geocell + aggregate (heavy duty) | HDPE 1.6mm, cell H 200–300mm, ⌀~300mm | Meyerhof only | KCS 11 30 10 |

Common to all four: aggregate grading envelope (Dmax≤100mm, fines<5mm≤15%, <2mm≤5%,
Dmax/D80≥3, Cg 0.7–1.3, Cu 1.7–5); lift ≤300mm; plate load test QC (min. 1, location by
agreement); 3–4m weathered-rock over-excavation rule (geocell products) at soil/rock interface.
