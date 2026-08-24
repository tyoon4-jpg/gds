
> **STATUS: DRAFT — PENDING RESPONSIBLE ENGINEER'S REVIEW AND SIGN-OFF**
> This record is compiled by the QA/QC sub-agent from the design/safety/construction findings
> assembled so far in this design-zone review. It is **not** an approved design zone record.
> Several fields are explicitly incomplete (marked **PENDING**) and must not be treated as final
> figures. No plant shall be positioned or mobilized on this zone until the design is finalized,
> the safety hold (below) is lifted, and this record is reissued with the responsible engineer's
> signature per PRD §6 Step 7 / §8.

# Design Zone Record — Appendix B (PRD `aggregate-working-platform-prd.md`)

**Record date:** 2026-08-24 (draft compiled)
**Compiled by:** platform-qaqc sub-agent, at request of site engineer
**Governing PRD revision:** Rev. A baseline + Rev. B grounding layer (`company-specs-summary.md`,
`design-worked-examples.md`)

---

## 1. Zone ID / Location Reference

- **Zone ID:** CRANE-PLATFORM-ZONE-01 *(placeholder ID — engineer to confirm against project
  zone-numbering convention/drawing register)*
- **Location:** Crane standing/working area for 50t crawler crane, erecting struts/walers on the
  MiPM excavation; working position approx. **6 m from the excavation crest** (nominal — to be
  confirmed against actual crane pad setout once track geometry is fixed).
- **Adjacent works:** Open MiPM deep excavation (soldier pile / waler / strut system) — zone sits
  within the fall/collapse envelope of an open excavation per PRD §7.1.

## 2. Governing Plant Item(s) and Load Case(s)

- **Governing plant:** 50-tonne crawler crane, working configuration (not travel configuration).
- **Manufacturer max static track bearing pressure:** 110 kPa (working configuration).
- **Dynamic/pitching amplification factor (Kdyn):** 1.15
- **Design applied bearing pressure:** **126.5 kPa** (110 × 1.15).
- **Track pad shoe width/length:** **PENDING** — not yet obtained from crane data sheet. Required
  to fix punching-shear plane geometry and contact-pressure distribution (PRD §5 Step 1).
- Other plant expected to traffic/stand on this zone (delivery vehicles, spotter vehicles, etc.)
  not yet confirmed — engineer to confirm whether any other plant item governs at any point in
  this zone's use.

## 3. Subgrade Characteristic Cu/CBR and Source of Data

- **Subgrade type:** Soft alluvial clay.
- **Characteristic Cu (near-surface):** 25 kPa.
- **Cu profile with depth:** **PENDING — open item, critical path.** Full-depth undrained shear
  strength profile has not yet been obtained. Per platform-construction's flag, this is the
  critical-path item blocking the whole zone from proceeding past PRD §6 Step 1.
- **Source of near-surface Cu value:** Not stated in inputs to date — engineer to confirm
  source/investigation reference (borehole, CPT, vane, or desk-study assumption) and whether it
  meets EN 1997-1/KDS 11 10 00 "characteristic (cautious) value" requirements.
- **Recommended supplementary investigation (per platform-qaqc's prior findings):** CPT and/or
  field vane profile with depth, supplemented by lab UU triaxial testing on recovered samples,
  with DCP infill for near-surface variability. Needed before the design thickness/LSF
  calculation in Section 6 below can be finalized.
- **CBR-equivalent (aggregate-only feasibility check):** ≈0.8% — used by platform-design to rule
  out an aggregate-only (unreinforced) platform as impractical on this subgrade.
- **Baseline condition survey:** A dated baseline condition survey of the currently exposed clay
  has been recommended (platform-qaqc) but not yet confirmed as completed — engineer to confirm
  and attach reference/date when available.
- **Weather protection status:** Positive drainage + light sacrificial cover of the exposed soft
  clay recommended by platform-construction pending construction start (to prevent rain-driven
  softening invalidating the design Cu before construction begins). Status of implementation:
  **PENDING confirmation** — log the date/method once in place.

## 4. Aggregate Type and Design φ'

- **Aggregate type:** 페블테크 (Pebble-Tech) well-graded crushed rock — aggregate-only option
  **ruled out** as impractical on this subgrade (see Section 3, CBR-equivalent ≈0.8%). Zone will
  use a geosynthetic-reinforced (geocell) platform per Section 5.
- **Design φ' (capping/platform aggregate layer):** Not yet finalized — typical company range
  40–45° for well-graded angular crushed rock per PRD §4.3; engineer to confirm specific product
  grading/source and certified φ' once selected.
- **Aggregate source approval:** **PENDING** — no source nominated yet in the inputs reviewed.

## 5. Geosynthetic Product and Design Properties (if used)

- **Reinforcement type:** Geocell (지오셀) — company's actual 하이셀/구속셀 product, not a flat
  geogrid/geotextile (per PRD §4.4 resolved note).
- **Product tier — leaning toward 구속셀 (1.6mm HDPE heavy-duty)** over standard 하이셀 (1.2mm
  HDPE), given excavation-edge proximity. **This selection is subject to PE (responsible
  engineer) judgment and is NOT finalized.**
- **Cell geometry (per company spec, product family default — to be confirmed for the selected
  tier):** cell height 200–300mm, internal cell diameter ~300mm, secured with 13mm deformed rebar
  stake pins, panel joints via geocell key (H-clip) or wire/cable ties.
- **Configuration:** Likely 2-stage geocell + Pebble-Tech capping layer, calibrated against the
  Seosan worked example (`design-worked-examples.md`) — order-of-magnitude only, **not
  finalized**.
- **Bearing design method:** Meyerhof only, per the product's 특별시방서 (company practice) —
  Giroud-Han/BR470-LSF framework used as international cross-check only, not the literal design
  basis (PRD §4.2 divergence note, §4.4 resolved note).

## 6. Calculated Required Thickness and Resulting LSF

- **Unreinforced (aggregate-only) Meyerhof bearing check:** qa1 ≈ 42.8 kPa vs. 126.5 kPa applied
  — **badly failing**, FS ≈ 0.34. Confirms aggregate-only is not viable (see Section 4).
- **Target LSF:** **1.5** (top band per PRD §4.2) — both the dynamic-load/piling-or-crane trigger
  and the soft-subgrade/excavation-edge trigger apply on this zone.
- **Expected geocell-reinforced platform thickness:** order-of-magnitude **≥500–550mm**
  (indicative only, calibrated against the Seosan worked example) — **NOT FINALIZED.**
- **Reason not finalized:** pending (a) full Cu-with-depth profile (Section 3) and (b) confirmed
  track pad shoe width/length (Section 2). Both are required inputs to close out the punching-shear
  and Meyerhof two-layer bearing calculations and lock the final thickness/LSF result.
- **Design method framing:** Confirmed as the PRD's primary temporary tracked-plant working
  platform application (BR470/LSF framing), not the permanent-foundation MOLIT application that
  the worked examples mostly cover — though platform-design cross-checked using both methods per
  PRD §4.2's divergence note.

## 7. Edge Distance and Slope Stability Check Result

- **Nominal edge distance:** ~6 m from excavation crest (crane working position) — **not yet
  confirmed adequate.**
- **Punching-shear-plane/slope-stability check (PRD §5 Step 5 / §7.1):** **NOT YET PERFORMED /
  RESULT PENDING.** This is an open safety hold item (see Section 9).
- **Geological contingency flag:** If a soil/weathered-rock transition is encountered within the
  zone, the geocell spec requires 3–4 m additional over-excavation at that interface, which could
  change the edge-distance geometry. This needs to be coordinated with the slope-stability check
  before either is finalized (per platform-safety's finding).
- **Risk register mapping (PRD §10):**
  - "Punching shear failure through platform into weak subgrade" — Likelihood Med, Severity High.
  - "Edge/slope instability near excavation" — Likelihood Low–Med, Severity Very High — **the
    open, unconfirmed item.**

## 8. Construction-Stage Verification Method and Hold-Point Sign-Off Record

- **Current PRD §6 stage:** Step 1 (pre-construction survey/clearance) — zone is **blocked from
  proceeding to Step 2** (subgrade preparation and verification).
- **Planned verification methods once design is finalized (PRD §5 Step 9, §6 Step 2, §8):**
  - Proof roll (visual), 100% of footprint.
  - DCP / plate load test (KS F 2444) — **mandatory** given crane + excavation-edge + soft-clay
    combination. Plate load test location to be **agreed with the supervising engineer at the
    critical crane-pad position near the crest**, not a generic grid point, per the company
    spec's "by agreement" clause (see frequency note below).
  - Field density testing during aggregate compaction, ≥95% max dry density (Modified
    Proctor/KS F 2312).
  - Proof-load/trial-pass verification of the completed platform (PRD §6 Step 6) before full
    crane operation — mandatory for this zone.
- **Frequency — PRD generic vs. company-spec actual (both stated; site's own approved ITP
  governs if one exists and differs from both):**
  - PRD §8 generic: min. 1 per design zone, 1 per 200–500 m².
  - Company 특별시방서 (실제 적용): min. 1 plate load test, location by agreement with the
    supervising engineer — **looser than the PRD grid**, but the actual project ITP (if approved
    and different) takes precedence contractually. Engineer to confirm whether a project-specific
    ITP exists for this zone.
- **Hold points recorded to date:**
  1. **HOLD — platform-safety, open.** Crane must not be positioned/mobilized until (a) the
     bearing/thickness redesign is finalized and (b) the punching-shear-plane/slope-stability
     check confirms whether 6 m edge distance is adequate. **Not lifted.**
  2. **Step 1→2 gate — open.** Full Cu-with-depth site investigation is the critical-path item
     for the whole zone (platform-construction). **Not passed.**
- **Sign-off record:** **NONE YET.** No hold point on this zone has been signed off. This section
  to be completed with engineer name, date, and test/inspection results as each stage clears.

---

## Summary of Open Items Blocking Finalization

| # | Open item | Owner / next action |
|---|---|---|
| 1 | Full Cu-with-depth subgrade profile (CPT/vane + lab UU triaxial + DCP infill) | Site investigation — critical path for entire zone |
| 2 | Crane track pad shoe width/length (manufacturer data) | Obtain from crane data sheet before thickness/LSF calc can close |
| 3 | Punching-shear-plane / slope-stability check at 6 m edge distance (PRD §5 Step 5 / §7.1) | platform-design + platform-safety — required before crane mobilization |
| 4 | Final geocell tier selection (하이셀 vs. 구속셀) and thickness/layer configuration | platform-design, PE judgment |
| 5 | Aggregate source/grading approval and certified φ' | platform-design / procurement |
| 6 | Baseline condition survey of exposed clay — confirm completed and dated | platform-construction |
| 7 | Weather-protection measure (drainage + sacrificial cover) — confirm implemented and log date/method | platform-construction |
| 8 | Confirm whether a project-specific approved ITP exists that overrides PRD/company-spec test frequency defaults | Site engineer / QA manager |
| 9 | Zone ID confirmation against project drawing/zone register | Site engineer |

**No plant shall be mobilized to this zone, and this record shall not be treated as approved,
until all items above are closed out, the design zone record is reissued with final figures, and
the responsible engineer signs off per PRD §6 Step 7 / §8.**
