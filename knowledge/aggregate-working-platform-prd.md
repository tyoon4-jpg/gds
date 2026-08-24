# PRODUCT REQUIREMENTS DOCUMENT — Aggregate Working Platform

페블테크 (Pebble-Tech) Aggregate Working Platform System — Design, Construction, and Safety
Requirements. **Primary application: ground improvement / working-platform support for building
foundations** (mat foundations, slab-on-grade). **Additional application: temporary tracked-plant
working platforms** in MiPM deep excavation and underground construction. Incorporating
geosynthetic/geocell reinforcement (하이셀/구속셀, Hi-Cell) design for both applications.

> Source of truth: `Aggregate_Working_Platform_PRD.docx` (repo root — note: despite the `.docx`
> extension this file is plain UTF-8 text, not a real Word binary). This markdown file is a
> structured mirror of that PRD for agent consumption (grep/read-friendly). If the two ever
> diverge, the `.docx` is authoritative; update this file to match.

- **Document status:** DRAFT — Rev. A
- **Date:** 2026-08-24
- **Note:** This PRD is a design/construction/safety procedure specification. It defines
  requirements and step-by-step procedures only — it is not a calculation-software spec.
- **Revision note (2026-08-24):** Scope corrected. The primary application of this system is
  **permanent building foundation ground improvement/support**; temporary tracked-plant working
  platform use (the original framing when this PRD was first drafted) is an **additional**
  application, not the primary one. This correction is reflected throughout this file and is
  consistent with the real reference material — see `knowledge/company-specs-summary.md` and
  `knowledge/design-worked-examples.md`, where every real project on file is a building
  foundation/mat/SOG ground-improvement job.

## 1. Purpose and Scope

Defines the design methodology, step-by-step construction procedure, and safety requirements for
the Aggregate Working Platform (페블테크) system — an engineered layer of well-graded crushed
aggregate, optionally reinforced with a geocell layer (하이셀/구속셀, Hi-Cell), placed over
prepared subgrade to improve ground bearing capacity and control settlement.

The system has **two applications**, covered together because they share the same materials,
design-method family, and construction procedure:

- **(a) PRIMARY APPLICATION — permanent building foundation support:** ground improvement
  beneath mat foundations, slab-on-grade (SOG), and isolated/strip footings for new-build
  structures, sized against sustained building loads and a permanent-structure settlement
  criterion.
- **(b) ADDITIONAL APPLICATION — temporary tracked-plant working platforms:** a temporary
  structural layer supporting tracked and wheeled plant — piling rigs, cranes, excavators,
  delivery vehicles — during temporary earth-retention and deep-excavation works under the MiPM
  underground construction system (soldier piles, waler beams, struts, rakers, diaphragm walls),
  sized against plant bearing pressure and a serviceability/leveling-tolerance criterion.

Both applications use the same aggregate/geocell products and the same field construction
procedure (§6–9); they differ in governing load case, target design method, and acceptance
criterion (§4.2). **Which application governs a given design zone must be identified explicitly
before sizing** — see §5, Step 1.

**In scope:** design methodology and bearing-capacity/settlement-sizing for both applications
(aggregate-only and geosynthetic/geocell-reinforced); step-by-step design procedure for both;
step-by-step field construction procedure (common to both); safety measures (design,
construction, in-service); QA/QC acceptance criteria, monitoring, and maintenance during service
life.

**Out of scope:** structural design of the permanent building superstructure/foundation elements
themselves (this PRD covers the ground-improvement layer beneath them, not the mat/footing/slab
structural design — that's the structural engineer of record's deliverable); deep foundation
design (e.g. 메가헬리컬파일 mega helical piles — a different system, its own spec); detailed
structural design of the built-up I-beam sections used in MiPM temporary works (separate MiPM
structural PRDs); software/calculation-tool implementation — no functions, scripts, or code are
to be implemented from this document.

## 2. Definitions

| Term | Definition | Korean |
|---|---|---|
| Aggregate Working Platform | Engineered layer of well-graded crushed rock aggregate over prepared subgrade — improves ground bearing capacity beneath permanent building foundations (primary application), or distributes plant loading as a safe, stable operating surface for tracked/wheeled equipment (additional application). | 페블테크 (Pebble-Tech) |
| Geosynthetic reinforcement | Geocell (지오셀) layer — 하이셀/구속셀 — placed at the subgrade/platform interface, or a flat geogrid/geotextile per the international BR470 framing, to provide separation, filtration, lateral restraint/confinement, and (for temporary platforms) tensile membrane reinforcement — reduces required platform thickness. | 하이셀 (Hi-Cell) / 구속셀 |
| Subgrade | Prepared, in-situ (or engineered fill) ground surface directly beneath the working platform. | — |
| LSF (Load Safety Factor) | Ratio of platform+subgrade bearing resistance to applied bearing pressure, per the BR470/TWf method used for the **additional (temporary tracked-plant) application only** (§4.2b). Target ≥1.0 min; ≥1.25 recommended where ground data uncertain or platform safety-critical. **The primary (building foundation) application uses a different acceptance basis** — allowable bearing capacity (FS=3.0 on qu) and a settlement limit, not an LSF ratio; see §4.2a. | — |
| Punching shear failure | Localized bearing failure mode: plant load punches through the aggregate platform into weaker subgrade before general (global) bearing failure develops. | — |
| Bearing pressure (ground contact pressure) | Vertical pressure applied to platform surface by tracked plant, crane outriggers, or wheel loads — static, dynamic, and pitching (eccentricity) effects (additional application); or sustained building load (primary application). | — |

## 3. Applicable Codes and Standards

| Domain | Korean | International | Notes |
|---|---|---|---|
| **Ground improvement design method (PRIMARY application — building foundation support)** | **KCS 11 30 10 (연약지반 치환공, soft-ground replacement); 국토교통부 구조물기초설계기준 Ch.4 (얕은기초); KS F 2444 (평판재하시험); KDS 11 50 05** | — (no direct international equivalent used; cross-checked against EN 1997-1 Annex D bearing-capacity theory) | Governing method for the primary application: allowable bearing capacity = lowest of Terzaghi/Meyerhof/empirical (KS F 2444 plate load test confirms in field); settlement = larger of Schmertmann/elastic theory, checked against a permanent-structure serviceability limit (typ. 25.4mm, confirm per project). See §4.2(a). |
| Working platform design method (ADDITIONAL application — temporary tracked-plant platform) | KDS 11 50 05 (얕은기초 지지력); KCS 11 20 20 (성토 및 다짐) | BR470 "Working Platforms for Tracked Plant" (2nd ed., 2019 TWf update); CIRIA C787 | BR470/TWf LSF/punching-shear method for the additional application; KDS bearing-capacity clauses verify subgrade ULS independently. See §4.2(b). |
| General geotechnical design (ULS/SLS) | KDS 11 10 00 (지반 설계 일반) | EN 1997-1 (Eurocode 7); AASHTO LRFD Bridge Design §10 | Partial factor / limit-state cross-check. |
| Bearing capacity theory | KDS 11 50 05 | Terzaghi / Meyerhof / Hansen; EN 1997-1 Annex D | BR470 punching-shear check builds on Meyerhof's two-layer method. |
| Compaction / earthworks | KCS 11 20 20; KS F 2312 (다짐시험) | EN 13286; ASTM D1557 (Modified Proctor); AASHTO T180 | Aggregate compaction QC, both applications. |
| Geosynthetics (하이셀/구속셀) reinforcement design | KS K ISO 10318; KDS 11 80 05 (보강토) | EN 13251; ISO 10318; Giroud–Han (geogrid-reinforced unpaved roads); AASHTO GRS guideline | Additional application: Giroud–Han method or manufacturer charts. Primary application: geocell confinement + stress-distribution increment added directly to allowable bearing capacity — see `company-specs-summary.md`. |
| Geosynthetics — index & durability testing | KS K ISO 10319 (인장강도); KS K ISO 12236 (CBR관입) | EN ISO 10319; EN ISO 12236; EN ISO 13438 | Product certification basis. |
| Plant/crane ground bearing pressure (additional application) | 산업안전보건기준에 관한 규칙 | BS 7121 Parts 1 & 11; LOLER/PUWER (UK, methodology reference only) | Crane manufacturer outrigger load data governs. |
| Site investigation / subgrade strength | KS F 2314 (CBR시험); KDS 11 10 05 | BS 1377; ASTM D1883 (CBR); ASTM D6635 (DCP) | Subgrade Cu/CBR characterization, both applications. |
| Health & safety (construction) | 산업안전보건법 및 시행규칙; KOSHA GUIDE | HSE (UK); OSHA 29 CFR 1926 | Applied to platform construction and plant-operation safety (§7). |

## 4. Design Basis

### 4.1 Functional Requirements

The platform/improved ground is designed for the governing (maximum) load case applicable to its
application (§1):

**Primary application (building foundation support):**
- Sustained dead and live load from the building's mat foundation, slab-on-grade, or footings,
  per the structural engineer's foundation loading schedule — the ordinary governing case.
- Any construction-stage surcharge from formwork, shoring, or material laydown on the slab/mat
  area before the structure is complete.

**Additional application (temporary tracked-plant platform)**, governing where this application
applies to a zone:
- Piling/soldier-pile installation rig (rotary, CFA, vibratory) — max outrigger/track reaction
  during pitching (leveling) and pile extraction.
- Mobile/crawler crane for strut/raker/waler erection — at working radius/config producing max
  outrigger or track pressure.
- Tracked excavator (bulk dig, trimming) at max digging/slewing reach.
- Delivery vehicles (concrete trucks, low-loaders) — wheel loads, often governing at edges/ramps.
- Surcharge from stockpiled materials (soldier pile sections, strut/waler steel, spoil).

A zone may need to be checked against **both applications in sequence** (e.g. a platform used
temporarily by a piling rig, later built over as the permanent mat's ground improvement) — see
§5, Step 1.

### 4.2 Design Method Overview

Two design methods apply, one per application (§1). **Identify which application governs a given
zone before selecting the method** — do not default to one without checking (§5, Step 1).

**(a) PRIMARY APPLICATION — building foundation support:** sized per KCS 11 30 10 (연약지반
치환공) and 국토교통부 구조물기초설계기준 Ch.4 (얕은기초), using two independent checks, both of
which must pass:

- **Bearing capacity:** ultimate bearing capacity qu computed by Terzaghi, Meyerhof, and an
  empirical formula (하이셀/구속셀-only zones: Meyerhof alone); the **lowest** governs. Allowable
  bearing capacity qa = qu ÷ 3 (safety factor 3.0 on ultimate capacity). Passes where qa ≥
  applied bearing pressure from the building load case (§4.1).
- **Settlement:** larger of Schmertmann's method and elastic theory (plus 1D consolidation where
  a compressible clay layer is present), checked against the project's permanent-structure
  serviceability limit — typically **25.4mm (1 inch)** total settlement, confirm the actual
  project-specific limit with the structural engineer.

Where a geocell (하이셀/구속셀) layer is used, its bearing-capacity contribution is added per §4.4
before the qa ≥ applied-pressure check, and its stiffness is reflected in settlement via an
equivalent modulus for the reinforced layer.

**(b) ADDITIONAL APPLICATION — temporary tracked-plant working platform:** sized using the
BR470/TWf (2019) load-spread and punching-shear method: applied plant bearing pressure checked
against combined resistance of (i) shear within the aggregate platform along assumed
punching-shear planes, and (ii) bearing resistance of the underlying subgrade at the base of
those planes. Cross-checked against classical bearing-capacity theory (Terzaghi/Meyerhof, per
KDS 11 50 05/EN 1997-1 Annex D). Governing criterion:

**LSF = (Platform punching-shear resistance + Subgrade bearing resistance) / Applied bearing pressure**

- LSF ≥ 1.0 — absolute minimum; only where subgrade strength and plant loads are both
  well-characterized and platform is not safety-critical.
- LSF ≥ 1.25 — recommended minimum for piling-rig and crane platforms, and wherever ground data
  derives from desk-study/limited investigation.
- LSF ≥ 1.5 — recommended where subgrade has soft/organic pockets, made ground, or where
  excavation proximity reduces passive resistance on one side of the punching-shear plane
  (edge-of-excavation condition).

**The two methods are not interchangeable substitutes for each other** — a zone governed by the
primary (building) application is checked against (a), not the LSF ratio in (b), and vice versa.
Where a zone is genuinely subject to both applications in sequence, size it against both and
carry the governing (thicker/more conservative) result forward.

> **Practical guidance for the design agent:** for a question about a real project deliverable,
> default to presenting method (a) — this is both the PRD's primary application *and* what every
> real company 검토서/계산서 on file actually runs (see `company-specs-summary.md`). Use method
> (b) when the question is specifically about a temporary tracked-plant platform, or when BR470
> LSF framing is explicitly requested. If unclear which application governs, ask.

### 4.3 Key Design Parameters (additional application)

The parameters and target LSF below are for the **additional (temporary tracked-plant)
application's** BR470 method (§4.2b). For the **primary (building foundation) application's**
parameters (subgrade γ/c/φ/E by layer, building design load, permanent-structure settlement
limit) and its FS=3.0-on-qu / Schmertmann-elastic-settlement acceptance basis, see §4.2(a) and
the worked examples in `knowledge/design-worked-examples.md`.

| Parameter | Symbol | Typical Source / Notes |
|---|---|---|
| Subgrade undrained shear strength | Cu | Site investigation (CPT/vane/lab UU triaxial); characteristic (cautious) value, not mean, per EN 1997-1. |
| Subgrade CBR (granular/cohesionless subgrade) | CBR | In-situ DCP or lab CBR (KS F 2314/ASTM D1883); Cu ≈ 30 × CBR (kPa) indicative correlation. |
| Platform aggregate friction angle | φ'platform | Well-graded crushed rock, compacted; typ. φ' = 40–45°. |
| Platform aggregate effective cohesion | c'platform | 0 (unbound granular) unless stabilized. |
| Punching-shear angle (load spread) | θ | BR470 default: vertical-sided plane (θ=0°), or full φ'-based spread if refined method used. |
| Track/outrigger contact pressure (static) | q0 | Manufacturer data sheet for the specific rig/crane and configuration — governing case, not nominal. |
| Dynamic/pitching amplification factor | Kdyn | Per BR470 guidance, typ. 1.1–1.3; piling rig "pitching" during installation is a governing dynamic case. |
| Platform thickness | h | Design output — governing (max) value from LSF check across all plant/load cases and subgrade zones. |
| Target LSF (additional application only) | LSF | Per §4.2(b) — min 1.0, recommended 1.25–1.5 by application; **not applicable to the primary (building) application**, which uses the FS=3.0 bearing-capacity/settlement basis of §4.2(a) instead. |
| Minimum platform edge distance from excavation/slope crest | de | Per §7.1 — geotechnical stability check independent of LSF bearing check. |

### 4.4 Geosynthetic Reinforcement (하이셀/구속셀) Design

Where aggregate-only thickness is impractical (excessive import volume, program duration,
headroom constraint), a geosynthetic/geocell layer (하이셀/구속셀) is introduced at the
platform/subgrade interface, or as a secondary layer within the aggregate:

- **Separation and filtration** — prevents subgrade fines migrating into/contaminating the
  aggregate.
- **Lateral restraint/confinement** — geocell/geogrid interlock with aggregate increases
  effective friction angle and lateral stiffness above it.
- **Membrane (tensioned-membrane) support** — very soft subgrades: reinforcement mobilizes
  tensile membrane action, adding a vertical resistance component (additional application).
- **Local base reinforcement / bearing capacity improvement** — quantified via Giroud–Han (2004)
  method (additional application) or the geocell manufacturer's certified confinement
  coefficient added directly to allowable bearing capacity (primary application).

For the **additional (temporary tracked-plant) application**, the geosynthetic-reinforced
platform is designed using the same LSF framework as §4.2(b), with the punching-shear resistance
term increased by the reinforcement contribution per Giroud–Han (or manufacturer's certified
design charts). For the **primary (building foundation) application**, the geocell's
bearing-capacity contribution is instead added directly to the allowable bearing capacity per
§4.2(a) (confinement + stress-distribution increment) before the qa ≥ applied-pressure check.

Typical outcome, either application: 20–30% reduction in required aggregate thickness for
equivalent capacity — in practice, on very soft subgrade, the reduction can be much larger
because an aggregate-only section becomes impractically thick rather than merely thicker (see
`design-worked-examples.md`).

> **Product note (resolved from original `[GDS-PENDING]`):** the actual 하이셀/구속셀ㅡ product is
> a **geocell (지오셀)**: HDPE sheet 1.2mm thick (구속셀 variant: 1.6mm), cell height 200–300mm,
> internal cell diameter ~300mm, secured with 13mm deformed rebar stake pins, panel joints via
> geocell key (H-clip) or wire/cable ties. See `company-specs-summary.md` for full spec.

## 5. Step-by-Step Design Procedure

> **Note:** the numbered steps below are written for the additional (temporary tracked-plant)
> application (§4.2b) and use plant-loading language throughout. For the primary (building
> foundation) application, the equivalent procedure follows the same overall shape (define loads
> → characterize subgrade → select aggregate/geocell → calculate → check edge/slope conditions
> where relevant → check settlement → drainage → document → construction-stage verification) but
> substitutes the building load case (§4.1) and the bearing-capacity/settlement method of
> §4.2(a) at Steps 1 and 4; see `design-worked-examples.md` for the primary application's
> procedure as actually run on real projects, pending a full Rev. B rewrite of this section to
> state both applications' steps explicitly.

Applies per platform design zone (areas of differing subgrade condition, plant type, or
excavation proximity are separate zones). Procedural specification — calculation performed by
the responsible geotechnical/structural engineer using §4 methods; no calculation software
implemented.

1. **Define plant and loading inputs** — manufacturer ground-bearing-pressure data for every
   plant item; governing (max) static contact pressure + dynamic/pitching factor per item;
   confirm track/outrigger/wheel contact dimensions and spacing (pad size, track
   length/width, mat size if outrigger mats used).
2. **Characterize subgrade** — review site investigation data (borehole logs, CPTs, trial pits);
   commission supplementary investigation where sparse; derive characteristic (cautious) Cu or
   CBR per zone per EN 1997-1/KDS 11 10 00; identify soft spots, made ground, organic material,
   groundwater conditions.
3. **Select platform aggregate and (if applicable) geosynthetic** — select
   grading/type (well-graded angular crushed rock, Type 1 sub-base equivalent), confirm φ';
   determine if geosynthetic (하이셀) needed per program/headroom/import-volume constraints
   (§4.4); select product class and obtain certified design parameters.
4. **Calculate required platform thickness (LSF check)** — per zone and governing plant load
   case: applied bearing pressure (incl. dynamic/pitching amplification); punching-shear
   resistance + subgrade bearing resistance per BR470/TWf (§4.2), incl. geosynthetic
   contribution where used (§4.4); iterate thickness until target LSF met; cross-check governing
   thickness against classical two-layer bearing-capacity theory (Meyerhof).
5. **Check platform edge and slope stability** — minimum edge distance from plant operating
   envelope to excavation crest/slope, per §7.1, accounting for reduced passive resistance where
   the punching-shear plane daylights into the excavation; global slope stability of platform +
   excavation edge under plant surcharge (limit-equilibrium per KDS 11 70 00/EN 1997-1).
6. **Check settlement and serviceability** — estimate total/differential settlement under
   sustained plant loading (e.g. crane standing for extended pick), particularly over variable
   subgrade; confirm compatibility with plant leveling tolerance; specify transition zone
   (tapered thickness or extra reinforcement) where differential settlement risk is high.
7. **Define drainage and groundwater control** — surface falls (typ. 2–3%) and
   perimeter/cross-fall drainage shedding water off the platform and away from the excavation;
   drainage blanket/cut-off drain/dewatering where groundwater/perched water is near formation
   level.
8. **Document design outputs** — design drawings (thickness by zone, geosynthetic layer
   extents/laps, drainage falls, edge distances, exclusion zones); design basis report
   (assumptions, characteristic values, LSF results by zone/load case, residual risks/ground-data
   limitations).
9. **Define construction-stage verification requirements** — field verification methods (proof
   rolling, plate load test, DCP) to confirm as-built subgrade strength before aggregate
   placement (see §6 Step 2, §8); trigger criteria and remedial procedure (sub-excavate and
   replace, increase thickness, add/upgrade geosynthetic) if field verification reveals subgrade
   below the design characteristic value.

## 6. Step-by-Step Construction Procedure

Applies per platform zone. Work shall not proceed to the next step until the preceding step's
acceptance criteria (§8) are met and recorded.

1. **Pre-construction survey and clearance** — confirm existing utilities/services within and
   adjacent to footprint (utility survey, trial holes at crossing points), mark/protect/divert;
   survey existing ground levels vs. design formation level/cut-fill; establish exclusion zones
   and site access/egress routes before plant mobilization (§7.2).
2. **Subgrade preparation and verification** — strip topsoil/unsuitable material to design
   formation level; remove soft spots/organic material/debris, backfill with approved granular
   material compacted per Step 4; proof-roll exposed subgrade with loaded dump truck/roller
   under engineer supervision (watch for rutting, pumping, deflection); DCP or plate load
   testing at frequency per design (typ. 1 per 200–500 m² or per zone, min. 1 per platform);
   report any subgrade below design assumptions to the design engineer immediately — do not
   proceed until revised design issued/approved.
3. **Geosynthetic (하이셀) installation, where specified** — confirm delivered product matches
   specified type/grade/certified properties; lay directly on prepared, verified subgrade,
   strong (machine) direction as specified; overlap adjacent panels per design (typ. 300–600mm
   on firm subgrade, up to 1.0m or mechanically jointed for very soft subgrade/geogrid under
   high load), in direction of aggregate placement/plant travel; avoid trafficking exposed
   geosynthetic, protect from UV/mechanical damage, cover within certified timeframe (typ. same
   shift); repair tears/punctures per manufacturer procedure before covering.
4. **Aggregate placement and compaction** — place in horizontal lifts not exceeding max
   compacted lift thickness per spec (typ. 150–300mm loose); work from geosynthetic-covered area
   outward; tip/spread with low-ground-pressure plant, avoid turning/sharp maneuvers on
   geosynthetic before first lift compacted; compact each lift (vibrating roller/plate) to
   specified relative compaction (≥95% max dry density, Modified Proctor/KS F 2312) before next
   lift; verify by field density testing per QA/QC plan (§8); repeat until design thickness
   achieved across full footprint incl. edges/transition/ramp zones.
5. **Surface finishing and drainage** — trim/grade to design falls (typ. 2–3% cross-fall)
   directing water away from excavation edge to drainage points; construct perimeter drainage
   (cut-off drains, swales) and drainage blanket outlets, discharging to an approved point (not
   into the open excavation); install edge protection, barriers, signage (§7.3) before opening
   to plant traffic.
6. **Verification (proof load) testing of the completed platform** — where specified (typ.
   piling-rig/crane platforms): plate load test or trial pass with actual/representative plant
   at critical locations, confirming no excessive rutting/deflection/visible distress; record
   results, obtain design engineer sign-off before full plant operation.
7. **Handover** — compile as-built records (thickness by zone, compaction test results,
   geosynthetic installation records, proof-test results), issue platform handover certificate
   confirming fitness for design plant loads and identifying use restrictions (max outrigger
   load, excluded zones, max plant travel speed); communicate approved use envelope to all plant
   operators and the temporary works coordinator before use commences.

## 7. Safety Measures

### 7.1 Design-Stage

- Minimum edge distance between plant operating envelope and excavation crest, based on
  punching-shear plane geometry and slope-stability check (§5 Step 5) — never based on bearing
  capacity alone.
- Higher target LSF band (≥1.25–1.5, §4.2) for safety-critical platforms: piling rigs (high
  center of gravity, dynamic pitching loads), and any platform within the fall/collapse zone of
  an open excavation.
- Design for worst-credible subgrade condition per zone, not the average — characteristic
  (cautious) values per EN 1997-1/KDS 11 10 00.
- Flag zones requiring construction-stage verification (proof rolling, plate load testing) as a
  mandatory hold point in design documentation (§5 Step 9).
- Documented contingency/remedial procedure for subgrade weaker than design assumptions, so
  field teams aren't making ad hoc decisions under time pressure.

### 7.2 Construction-Stage

- No plant traffics the platform footprint until subgrade verification (§6 Step 2) is complete
  and formally accepted.
- Maintain exclusion zones around active placement/compaction operations; banksmen/spotters for
  all plant reversing or working near the excavation edge.
- Prohibit plant/personnel standing on or trafficking exposed (uncovered) geosynthetic, beyond
  the minimum necessary for installation.
- Enforce minimum edge/barrier setback during construction consistent with design edge distance
  (§7.1); do not reduce for temporary construction convenience without engineer approval.
- Inspect each completed lift for compaction, thickness, level before covering with next lift or
  opening to plant traffic — do not proceed on an unverified lift.
- Proof-load/trial-pass verification (§6 Step 6) under exclusion-zone conditions, only essential
  personnel present.
- Maintain positive drainage throughout construction; no ponding on the partially completed
  platform (can locally soften aggregate/subgrade).

### 7.3 In-Service (Operational)

- Display approved use envelope (max outrigger/track load, excluded zones, max travel speed,
  one-way/two-way routes) at platform access points; communicate in plant operators' site
  induction.
- Routine visual inspection (rutting, cracking, ponding, edge erosion) at frequency proportional
  to usage intensity — minimum daily during active piling/crane operations.
- Re-verify (visual + spot compaction/level check) after heavy rainfall, freeze-thaw cycle, or
  extended plant standing load, before resuming full operations.
- Maintain surface drainage falls throughout service life; repair rutting/ponding promptly with
  compacted aggregate reinstatement, not by blading/regrading without compaction.
- Prohibit excavation/trenching/service installation through the platform without a
  permit-to-work and reinstatement procedure agreed with the temporary works coordinator.
- Monitor for edge instability (tension cracks, bulging) near the excavation crest; stop plant
  operations in the affected zone immediately, notify temporary works coordinator/designer.
- Where platform supports a piling rig or crane at a fixed position for an extended duration,
  monitor progressive settlement (periodic level survey), act on any trend exceeding the design
  serviceability limit (§5 Step 6).
- Decommission and reinstate (or formally hand over as permanent works if applicable) at end of
  service life per §9.

> These are procedural minimums consistent with 산업안전보건법/KOSHA guidance and international
> practice (HSE/OSHA); project-specific TWP and the site's H&S plan take precedence where more
> stringent.

## 8. QA/QC and Acceptance Criteria

| Stage | Test / Check | Frequency | Acceptance Criterion |
|---|---|---|---|
| Subgrade | Proof roll (visual) | 100% of footprint | No visible rutting, pumping, or deflection under loaded vehicle. |
| Subgrade | DCP / plate load test | Min. 1 per design zone; 1 per 200–500 m² | ≥ design characteristic Cu/CBR. |
| Geosynthetic | Product certificate check | Each delivery/batch | Matches specified type/grade; certified properties on file. |
| Geosynthetic | Installation inspection | 100% visual, continuous during laying | Correct orientation, overlap ≥ specified minimum, no tears/damage, covered within specified time. |
| Aggregate | Grading / source approval | Each source / as specified | Conforms to specified grading envelope (e.g. Type 1 equivalent). |
| Aggregate compaction | Field density test | Min. 1 per lift per 200–500 m² (or as specified) | ≥95% max dry density (Modified Proctor/KS F 2312), or as specified. |
| Platform level/thickness | Survey | Grid survey on completion of each zone | As-built thickness ≥ design thickness (tolerance −0/+ per spec); falls within ±0.5% of design fall. |
| Platform performance | Proof-load / trial pass (critical platforms) | Once, prior to full operational use | No excessive rutting/deflection; engineer sign-off recorded. |
| In-service | Routine visual inspection | Daily during active use (min. weekly otherwise) | No rutting > specified limit, no ponding, no edge distress. |

> **Company-practice note:** per the 특별시방서 (페블테크/하이셀/조립골재/구속셀), the actual
> plate load test (KS F 2444) requirement is looser than this table — typically stated as
> "minimum 1 test, location by agreement with the supervising engineer," not the PRD's 1-per
> 200–500 m² grid. When advising on-site, present the PRD's grid frequency as the recommended
> minimum and confirm actual project-specific ITP/QA plan frequency, since it may be governed by
> the site's own specification rather than this PRD.

## 9. Maintenance, Monitoring and Decommissioning

- **Maintenance:** reinstate rutted/degraded areas promptly (remove disturbed material,
  re-compact in lifts, re-test per §8) rather than overlaying loose material on a soft base;
  maintain/clear drainage falls, cut-off drains, outlets (sediment/debris blockage is a common
  cause of localized softening); reassess design if plant type/load/operating position changes
  from original basis before that plant is deployed.
- **Periodic monitoring:** level survey at frequency matched to observed settlement trend and
  criticality (e.g. monthly for platforms supporting long-duration crane standing loads); visual
  condition survey concurrent with routine temporary works inspections.
- **Decommissioning:** remove aggregate (and geosynthetic, unless left in place by design as
  part of a permanent working surface), reinstate per permanent works/landscaping requirements;
  where geosynthetic left in place, record location/extent in as-built/handover records; close
  out and archive all QA/QC, monitoring, inspection records in the temporary works close-out
  file.

## 10. Risk Register (Summary)

| Hazard | Potential Consequence | Likelihood* | Severity* | Primary Mitigation |
|---|---|---|---|---|
| Punching shear failure through platform into weak subgrade | Plant tips/sinks; injury, plant loss, delay | Med | High | LSF design (§4.2) with characteristic subgrade values + construction-stage verification (§6 Step 2). |
| Undetected soft spot / made ground | Localized platform failure | Med | High | Site investigation coverage + proof rolling/DCP at construction stage (§6 Step 2). |
| Edge/slope instability near excavation | Platform or plant collapse into excavation | Low–Med | Very High | Minimum edge distance + slope stability check (§5 Step 5) + monitoring (§7.3). |
| Geosynthetic damage/incorrect installation | Loss of reinforcement benefit; localized under-design | Med | Med | Installation inspection + repair procedure (§6 Step 3). |
| Water ingress / poor drainage | Subgrade softening, reduced LSF over time | Med | Med | Drainage design (§5 Step 7) + maintenance (§9). |
| Plant exceeding design load envelope | Bearing failure, tip-over | Low–Med | High | Communicated use envelope + site induction (§7.3). |
| Differential settlement across subgrade transition | Plant instability/mal-level | Low | Med | Transition zone design + monitoring (§5 Step 6). |

*Likelihood/Severity are indicative categories for illustration; project-specific risk
assessment should be carried out per the site's risk assessment procedure and recorded
separately.

## 11. References

1. BRE/TWf. BR470 — Working Platforms for Tracked Plant, 2nd ed. (2019 update).
2. CIRIA C787 — temporary works platforms and ground engineering guidance.
3. KDS 11 10 00 — 지반 설계기준 (일반사항).
4. KDS 11 50 05 — 얕은기초 설계기준.
5. KDS 11 80 05 — 보강토옹벽 설계기준 (reinforcement design cross-reference).
6. KCS 11 20 20 — 성토 및 다짐 표준시방서.
7. EN 1997-1:2004+A1 — Eurocode 7, Part 1: General rules.
8. EN 13251, ISO 10318, EN ISO 10319, EN ISO 12236 — geosynthetics terminology/test standards.
9. Giroud, J.P. and Han, J. (2004). "Design Method for Geogrid-Reinforced Unpaved Roads." ASCE.
10. BS 7121 — safe use of cranes (Parts 1 and 11).
11. KS F 2312, KS F 2314 — 다짐시험, CBR시험.
12. 산업안전보건법 및 산업안전보건기준에 관한 규칙; KOSHA GUIDE.
13. KCS 11 30 10 — 연약지반 치환공 표준시방서 (governs the primary application, §4.2a); MOLIT
    구조물기초설계기준(해설) Ch.4 얕은기초; KS F 2444 — 평판재하시험; KS F 2502 — 체가름시험;
    KS F 2511 — 흙의 0.08mm체 통과량 시험.

## Appendix A — Aggregate-Only vs. Geosynthetic-Reinforced Platform

| Criterion | Aggregate-Only | Geosynthetic-Reinforced (하이셀/구속셀) |
|---|---|---|
| Required thickness (typ.) | Baseline (per applicable §4.2 check) | ~20–30% thinner for equivalent capacity/LSF |
| Import aggregate volume/cost | Higher | Lower aggregate cost, offset by geosynthetic material + installation cost |
| Program/construction speed | Simple, fast, no laying sequence constraint | Requires careful laying/overlap sequence; slower per zone but net faster where thickness reduction shortens overall earthworks |
| Performance on soft/variable subgrade | Requires greater thickness to compensate; more prone to punching on soft pockets | Better — separation prevents fines contamination; reinforcement improves punching resistance directly |
| Suitability for very soft subgrade | May become impractical (excessive thickness) | Preferred; membrane/reinforcement action essential |
| Headroom-constrained sites | Limited by required thickness | Preferred where reduced thickness needed for clearance |
| Sensitivity to installation quality | Low — mainly compaction QC | Higher — orientation, overlap, damage during laying materially affect performance |
| Removability/reuse at decommissioning | Aggregate reusable elsewhere | Geosynthetic typically not reusable; may be left in place or disposed |
| Typical application | Both applications; firm subgrade or short-duration additional-application platforms | Both applications, especially soft/variable subgrade (primary) or piling rig/crane platforms on soft ground (additional) |

## Appendix B — Design Zone Record Template

Fields to complete per platform design zone (blank template/form to be issued alongside this
PRD for field/design-office use — no calculation logic embedded here):

- Zone ID / location reference
- Applicable design application(s) — primary (building), additional (tracked-plant), or both
- Governing load case (building load schedule, or plant item(s)/load case(s))
- Subgrade characteristic Cu/CBR and source of data
- Aggregate type and design φ'
- Geosynthetic product and design properties (if used)
- Calculated result — allowable bearing capacity vs. applied pressure and settlement vs. limit
  (primary application), or required thickness and resulting LSF (additional application)
- Edge distance and slope stability check result (additional application, or where a primary
  zone is also excavation-adjacent)
- Construction-stage verification method and hold-point sign-off record

## Appendix C — GDS Reference Files (status: resolved)

Originally noted that GDS reference files at `c:/Users/user/my-projects/gds` were not accessible
from the drafting environment; no content from that folder had been incorporated into Rev. A.

**Update:** the reference folder has since been reviewed (see `GDS_spec/` in this repo — company
특별시방서 for 페블테크/하이셀/조립골재/구속셀/메가헬리컬파일, and real project
검토서/계산서/시공계획서). Findings are captured in `knowledge/company-specs-summary.md` and
`knowledge/design-worked-examples.md`. **This review is what surfaced the scope correction above:
every real project on file is a primary-application (building foundation) job**, which is why
this PRD's scope statement (§1) and design method overview (§4.2) were restructured to lead with
that application rather than treat it as a secondary finding.
