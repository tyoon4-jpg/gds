# Real Project Worked Examples

Extracted directly from the actual project design/review/calculation packages under `GDS_spec/`
(검토서 = review report, 계산서 = calculation report, 시공계획서 = construction plan) — five real
projects using 페블테크 (aggregate-only) and 하이셀 (geocell-reinforced) platforms, plus one real
approved construction plan. These are the numbers a site engineer's own project should look like
if it's following the company's normal practice. **Always re-read the source PDF/xlsx for a
figure that will be quoted in a contractual or safety-critical document** — this file is a
navigation aid, not the record of record.

Source documents:
- `GDS_spec/1.2.250718 전북 전주시 완산구 상림동 596 다세대주택 신축공사 페블테크 검토서.xlsx` (Jeonju)
- `GDS_spec/1.3.250801 LIG넥스원 구미H 5레이더시험장 구축공사 페블테크 검토서.xlsx` (Gumi)
- `GDS_spec/260728 광주 광산구 월전동 (주)디엔 공장 신축공사 하이셀 검토서.pdf` (Gwangju)
- `GDS_spec/3.260629 충남 서산시 수석동 1156 대원산업 3공장 증축공사 하이셀 계산서.pdf` (Seosan)
- `GDS_spec/26.07 하이셀 시공계획서 충남 공주 금흥2지구 공동주택 신축공사_수정.pdf` (Gongju — approved construction plan, not a design calc)

Engineer of record on the calc packages: 토질 및 기초기술사 (licensed Soil & Foundation PE) —
강진기 (Gwangju, Seosan) or 김선학 (Jeonju, Gumi), of ㈜지반디자인앤솔루션. **Every design agent
answer should say a stamped calc from a licensed PE is required before construction — these
worked examples are for calibration, not a substitute for that stamp.**

## A. The calculation method, at formula level

This is what the company's own 검토서/계산서 actually run (see the divergence note in
`company-specs-summary.md` for why this differs from the PRD's BR470/TWf LSF framing). All five
projects follow this same structure.

### A.1 Unreinforced (original ground) bearing capacity

Meyerhof bearing capacity formula (per 구조물기초 설계기준 해설 2009, p.191):

```
qu = c·Nc·sc·dc + q·Nq·sq·dq + 0.5·γ·B·Nr·sr·dr
```
- `c` = subgrade cohesion, `φ` = friction angle → `Nc, Nq, Nr` bearing capacity factors
- `sc, sq, sr` = foundation shape factors (function of B/L)
- `dc, dq, dr` = depth factors (function of Df/B)
- `q` = effective overburden at foundation level (adjusted for groundwater per the 3-case
  Dw-vs-Df table in the calc sheets)
- Allowable bearing: **qa1 = qu / 3** (FS = 3.0 on ultimate capacity — note this is a different
  safety-factor convention from the PRD's LSF ratio; state which convention you're using).

Pebble-Tech/조립골재 특별시방서 also require Terzaghi and an empirical formula computed in
parallel, with the **lowest of the three governing**; 하이셀/구속셀 specs use Meyerhof only. In
every worked example below, the calc sheet only shows Meyerhof — treat that as this company's
practical default even on 페블테크-branded projects.

### A.2 Pebble-Tech (aggregate-only) contribution

Re-run the same Meyerhof formula with the foundation notionally raised to the top of the
aggregate layer (i.e. using the aggregate's own φ, typically 45°, and the reduced effective
depth to the *original* ground surface) → **qa2**. The aggregate-only increment is
**qa3 = qa2 − qa1**.

### A.3 Hi-Cell (geocell) reinforcement increment

This is the step that is *not* documented in the 하이셀 특별시방서 itself but appears in every
real calc package — the geocell's bearing-capacity contribution is computed as:

```
I = (IC + IS) / 2
qr  = qa1 + I                      (reinforced capacity, simple form)
qra = qa1 + qa3 + I                (reinforced capacity, combined with Pebble-Tech layer above it)
```
- `IC` = confinement-effect increment = `(Gfr · q · Gfr-factor)` — the geocell's lateral
  confinement raising the effective friction/stiffness of the fill immediately above it. (`Gfr`
  = Hi-Cell confinement coefficient from the product's certified data.)
- `IS` = stress-distribution-effect increment = `q'' − q0'`, where `q'' = q·B·L / (B'·L')` is the
  contact pressure re-spread over an enlarged effective footprint `B'×L'` at the base of the
  Hi-Cell layer, using a **50° spread angle** through the confined (Hi-Cell) zone.
- A second, shallower **26.6° spread angle** (= arctan 0.5, i.e. a 2-horizontal:1-vertical
  spread) is then used to project the Hi-Cell base contact pressure `q0'` further down onto the
  *original* subgrade, giving the original-ground contact pressure `q1'` that's checked against
  the plain qa1 capacity as a secondary confirmation.
- Allowable check: **qra (or qr) ≥ design load**, generally with the same implicit ~3× margin
  baked in from A.1 rather than a separately quoted safety factor.

**Design-agent guidance:** if you don't have the project's certified Hi-Cell `Gfr` value, say so
explicitly — do not assume a number. This increment is product-certification data, not a
constant you can look up from the PRD.

### A.4 Settlement

Two independent methods are both run, per project standard (구조물기초 설계기준해설
2009 p.247/252, and p.247 of the 2018 edition for consolidation):

1. **Schmertmann's method**: `S = C1·C2·Δq·Σ(Iz·Δz/Es)` — strain-influence-factor integration
   over the soil profile below the footing, with `C1` (depth correction) and `C2` (creep
   correction, `1 + 0.2·log(t/0.1)`, t in years — the sheets use t=30 giving `C2≈1.44`).
2. **Elastic theory**: `S = q·B·(1−ν²)/E · Is`, with `Is` from standard rigid/flexible
   center-point/corner-point influence-factor tables (reproduced in the calc sheets).
3. **Consolidation settlement** (clay layers only, Terzaghi one-dimensional): computed
   separately and *added* to whichever of (1)/(2) governs when a compressible clay layer is
   present in the profile (Seosan project — see B.3).
4. **Reinforced-layer's own elastic compression** (`Spt`) is computed for the Pebble-Tech/Hi-Cell
   layer itself using an equivalent modulus `Ea = E·(1−ν)/[(1+ν)(1−2ν)]` and added to the
   settlement of the *underlying* original ground (`S0`, computed the same way as step 1/2 but
   using the reduced net pressure reaching the original subgrade). Total reinforced settlement
   `Si = Spt + S0` (+ consolidation term if applicable).
- **Governing settlement = the larger of Schmertmann vs. elastic theory** (plus consolidation
  where applicable), per spec §2.2(3).
- **Acceptance criterion used in every project: total settlement ≤ 25.4 mm** (1 inch) — this is
  the company's standard serviceability limit for a permanent building foundation. **This is not
  the same criterion as the PRD's plant-manufacturer leveling-tolerance discussion (§5 Step 6)** —
  if the question is about a *temporary tracked-plant platform* rather than a *permanent
  foundation*, 25.4mm is a reasonable conservative default but confirm against the specific plant
  manufacturer's tolerance instead.

## B. The five worked examples

| Project | Type | Design load | Subgrade (governing layer) | System & thickness | Unreinforced qa | Reinforced qra | Settlement before → after (limit 25.4mm) |
|---|---|---|---|---|---|---|---|
| Jeonju 다세대주택 (housing, mat THK500) | Pebble-Tech only | 150 kPa | N=4–8/30 silty sand (SM) | Pebble-Tech 500mm + geotextile mat ×1 | N.G. (not separately quoted; weathered rock underlying is deep) | — (aggregate-only sizing, not incremental qra) | not itemized in summary sheet |
| Gumi LIG Nex1 radar site (mat THK1000) | Pebble-Tech only | 250 kPa | N=15–17/30 silty sand (SW), weak sandy layers to 45m | Pebble-Tech **1500mm** + geotextile mat ×1 | — | — | flagged differential-settlement risk vs. adjacent already-settled radar building |
| Gwangju DN factory — 작업장(workshop) BH-1 | Hi-Cell + Pebble-Tech | 150 kPa | γ=18, φ=21–23°, weathered soil/rock profile | Hi-Cell 200mm (1 stage) + Pebble-Tech 100mm (300mm total) + PET-MAT | 111.5 kPa (N.G.) | **181.6 kPa (O.K.)** | 43.9mm (N.G.) → **19.3mm (O.K.)** |
| Gwangju DN factory — 공장(SOG slab) BH-1 | Hi-Cell + Pebble-Tech | 100 kPa | same profile | Hi-Cell 200mm + Pebble-Tech 50mm (250mm total) + PET-MAT | 83.7 kPa (N.G.) | **128.2 kPa (O.K.)** | 34.0mm (N.G.) → **16.6mm (O.K.)** |
| Gwangju DN factory — 공장 BH-2 | Hi-Cell + Pebble-Tech | 100 kPa | similar profile, deeper weathered rock | (same system, calc continues past extracted page range) | 92.9 kPa (N.G., partial calc) | not fully captured — re-read source PDF pp.28–49 | not captured |
| Seosan Daewon Industry — 지상층 T450 | Hi-Cell (2-stage) + Pebble-Tech | 200 kPa | includes a soft silty-clay layer (c=16 kPa) | Hi-Cell 400mm/2 stages + Pebble-Tech 50mm (450mm total) + PET-MAT | 100.2 kPa (N.G.) | **233.8 kPa (O.K.)** | 84.0mm (N.G.) → **20.40mm (O.K., incl. consolidation)** |
| Seosan Daewon Industry — 지상층 T550 | Hi-Cell (2-stage) + Pebble-Tech | 200 kPa | same profile | Hi-Cell 400mm/2 stages + Pebble-Tech 150mm (550mm total) + PET-MAT | 100.2 kPa (N.G.) | **239.0 kPa (O.K.)** | 84.0mm (N.G.) → **20.08mm (O.K., incl. consolidation)** |

Notes on reading this table:
- "N.G." / "O.K." = 판정 (judgment) exactly as marked in the source calc sheets: N.G. = original
  ground fails the design load; O.K. = reinforced platform passes.
- Jeonju and Gumi are **aggregate-only** (no Hi-Cell) — note how much thicker the aggregate-only
  layer has to be (500mm at 150kPa on N=4–8 sand; 1500mm at 250kPa on similarly weak sand)
  compared to the Hi-Cell-reinforced cases achieving 150–200kPa on comparably or more poor
  subgrade (qa1 as low as 83.7–111.5 kPa) with only 250–550mm total. This is the concrete,
  project-scale evidence behind the PRD Appendix A claim that geocell reinforcement cuts required
  thickness — in these real cases the effective reduction (vs. what an equivalent-performance
  aggregate-only layer would need) is larger than the PRD's generic "20–30%" estimate for some
  subgrade conditions, because the aggregate-only option becomes impractically thick on very weak
  ground rather than merely 20–30% thicker.
- "Hi-Cell 400mm/2 stages" = two vertically stacked geocell courses (단수=2), each ~200mm cell
  height, consistent with `company-specs-summary.md`'s 200–300mm single-cell-height spec.

## C. Fully worked example — Gwangju DN factory, 작업장(workshop) BH-1

Use this as the reference calc walkthrough when explaining the method to a site engineer.

**Inputs**
- Foundation: mat, B=5.0m, L=8.0m, Df=0.65m, design load q0 = 150 kPa, groundwater at 3.2m
  (below the zone of influence for this check).
- Subgrade profile (γ in kN/m³, c in kPa, φ in °, E in kN/m²):
  fill 0–3.7m (γ18,c0,φ21,E9,000) / alluvium 3.7–7.8m (γ18,c0,φ23,E14,000) /
  weathered soil 7.8–18.0m (γ19,c5,φ25,E48,100) / soft rock 18.0–30.0m (γ20,c20,φ30,E210,000).
- Pebble-Tech aggregate: φ=45°, E=100,000–200,000 kN/m² (thickness-dependent in the sheet).
- Hi-Cell: 200mm (1 stage), E≈200,000–224,359 kN/m² (equivalent modulus).

**Step 1 — original ground bearing:** Meyerhof qu → qa1 = **111.5 kPa**. Design load 150 kPa >
111.5 kPa → **N.G.**

**Step 2 — with Pebble-Tech only (aggregate raises the effective founding level and spreads
load):** qa2 = 127.0 kPa → qa3 = qa2 − qa1 = **15.5 kPa** increment. Still short of 150 kPa on
its own.

**Step 3 — add Hi-Cell reinforcement increment:** confinement increment IC = 88.35 kPa
(`Gfr`-based), stress-distribution increment IS ≈ 20.76 kPa (spread at 50° through the Hi-Cell
zone) → I = (IC+IS)/2 = **54.55 kPa**. Combined: **qra = qa1 + qa3 + I = 111.5 + 15.5 + 54.55 ≈
181.6 kPa.** 181.6 kPa ≥ 150 kPa → **O.K.**, margin ≈ 21%.

**Step 4 — settlement:** Schmertmann on the unreinforced profile gives 43.9mm (N.G. against
25.4mm limit). With the reinforced section (Pebble-Tech 100mm + Hi-Cell 200mm spreading load into
the profile), recompute: reinforced-layer compression Spt ≈ 0.2mm (negligible — the aggregate/
geocell itself is stiff), underlying-ground settlement S0 = 16.46mm (Schmertmann) — take the
larger of Schmertmann (Si=19.11mm) vs. elastic theory (17.6→17.8mm total) → governing = **19.31mm
< 25.4mm → O.K.**

**Result:** 300mm total (Hi-Cell 200mm + Pebble-Tech 100mm) + PET-MAT ×1 satisfies both the
bearing-capacity check (181.6 vs 150 kPa) and the settlement check (19.3mm vs 25.4mm) for this
zone. This is the level of detail — governing case, both checks, explicit margin — a design-agent
answer should reproduce for a real sizing question.

## D. Real construction-plan precedent — Gongju 금흥2지구 공동주택

From the one **approved 시공계획서** (construction plan, not a design calc) in the reference set —
use this as a template structure and for realistic resourcing rates, not as a source of design
numbers.

**Scope:** 하이셀기초지반보강공사 (Hi-Cell foundation ground-reinforcement work), 공주 금흥2지구
A1블럭, buildings 101–107동 + 독립기초 (isolated footings). Hi-Cell area 9,571.26 m², thickness
300–350mm. Branded internally as the **"Puzzle Soil"** construction method.

**Process flow (공정흐름도):** 현황측량/규준틀설치(site survey/batter boards) → 토공사(earthworks,
main contractor's scope) → 원지반다짐(subgrade compaction) → 하이셀설치+골재반입(Hi-Cell
install + aggregate delivery) → 골재배합(on-site blending, ≥2 graded aggregate sources) →
포설&다짐(spread & compact) → PBT시험(plate load test, per §A/QC) → 포설면확대사진(as-built
photo record) → P.E필름 설치/현장정리(protective sheeting, site tidy, handover to next trade).

**Resource mobilization (33-day program, 9,571m² total)** — usable as a rough rate for
pro-rating a new site by area: staff 5/day, foreman+direct labor 4/day, signalmen 2/day;
excavator 0.6m³ ×2/day, 15t dump truck (as needed), compact excavator 0.2m³ ×1/day, 10t roller
×1/day, aggregate blending plant ×1/day; blended aggregate ≈125 m³/day, Hi-Cell ≈290 m²/day,
PET-MAT ≈290 m²/day.

**Daily safety cadence (실제 운영):** 07:30 안전조회/안전교육 (safety assembly/briefing) →
07:40 오전 TBM (morning toolbox meeting) → 09:00 순회점검 (patrol inspection) → 13:00 오후TBM →
15:00 순회점검 → 작업완료 10분전 작업장 정리정돈 (tidy-up before end of shift). Stated safety
KPIs: 재해 ZERO (zero incidents), TBM 실천율 100%, 위험예지활동 생활화 (habitual hazard
prediction activity).

**Hazard-specific controls by activity (안전작업 지도서), verbatim structure:**
- **토공사 (earthworks):** equipment-swing-radius collision; ground collapse from water inflow;
  slope/soil-condition inattention → dedicated signalman, drainage/pumping checks, safe slope
  gradient maintained during excavation.
- **하이셀 포설 / 배합골재 포설·다짐 (Hi-Cell & aggregate placement/compaction):** trip/fall at
  excavation-edge steps; worker struck by equipment in swing radius; ground collapse from water
  inflow; material drop during delivery → dedicated signalman + adequate clear work space,
  subgrade condition check before replacement, work-face exclusion zone, upper/lower signalman
  radio-confirm before unloading.
- **장비하역 및 인양 (equipment unloading / crane lifting):** dropped load; crane overturn; pinch
  injury under a suspended load; struck by falling debris → sling condition check (spec/damage),
  crane setup verified before use, exclusion zone + tag lines around lifted loads, check for loose
  attachments before lifting.

**Environmental control (bundled into the same plan):** dust suppression at dump-truck unloading
— wet down the load bed before tipping, keep the haul-road site entry/exit clean.

**QC reference:** the plan attaches a project-specific "하이셀기초 CHECK LIST" — recommend a site
engineer request or replicate an equivalent checklist rather than relying on the generic PRD §8
table alone.

## E. Practical flags for a real project (things easy to miss)

- **Headroom/clearance constraint** (Jeonju review notes): leave a minimum clear working height
  above the *finished Pebble-Tech surface* to any strut/waler bracing of **≥2.3m for a 3.5-ton
  combination roller**, or **≥3.2m for a 10-ton roller** — this directly constrains which
  compaction plant can be used under a MiPM strut/waler level, and should be checked against the
  temporary works bracing layout before committing to a compaction-plant class.
- **Scope split:** excavation/bulk earthworks to formation level is typically the **main
  contractor's (원도급사) scope**, not the aggregate-platform specialist subcontractor's — confirm
  this split explicitly before mobilizing, per the Jeonju review's stated assumption.
- **Differential settlement next to an existing structure** (Gumi LIG Nex1 case): where a new
  platform/foundation sits adjacent to an existing building that has already finished settling,
  flag the differential-settlement risk explicitly and mitigate by adjusting the new mat's target
  level or the Pebble-Tech thickness — don't assume uniform settlement across old/new construction
  boundaries.
- **Weathered-rock transition** (from `company-specs-summary.md`, confirmed in the Hi-Cell spec):
  over-excavate weathered rock an additional 3–4m before installing Hi-Cell/구속셀 wherever
  rockhead is encountered within the platform footprint — affects both program and excavation
  volume, easy to miss if the geotechnical profile isn't checked zone-by-zone.
- **No rubble base needed under lean concrete** when Pebble-Tech replacement is used underneath
  (Jeonju review note) — conventional 잡석(crushed rubble) sub-base beneath the blinding layer
  becomes redundant; flag this as a potential cost/spec conflict if the structural drawings still
  call for it.
- **Application mismatch to double-check with the requester:** all five worked examples above are
  **permanent building foundation / mat / SOG-slab ground improvement**, not literally a
  *temporary tracked-plant working platform* as framed in the PRD's primary scope (§1). The
  underlying aggregate/geocell system and company calculation method are the same either way, but
  confirm which application the site engineer actually means before quoting a design load,
  acceptance criterion (25.4mm vs. plant-manufacturer tolerance), or service-life expectation —
  see the divergence note in `company-specs-summary.md`.
