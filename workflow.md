# workflow.md — Site Engineer Lifecycle

How a site engineer takes an Aggregate Working Platform (페블테크/하이셀) zone from first
request to handover using this agentic program. Each stage names the sub-agent to use, the
governing PRD clause, the hold points that gate the next stage, and the record produced.

- **Router:** run `/aggregate-platform` when it's unclear which specialist applies, or just ask
  your question directly — the right sub-agent is picked automatically.
- **Safety-first override:** if anything describes an *active* platform hazard (rutting,
  ponding, a crack near the excavation crest, plant over its load envelope, subgrade weaker
  than assumed, a failed proof roll/test), go straight to `platform-safety` — do not wait to
  finish the stage you're on.
- **Ground rule (PRD §6):** work does not proceed to the next step until the current step's
  acceptance criteria (PRD §8) are met **and recorded**.
- **First question every time (PRD §5 Step 1):** which application governs this zone —
  primary (permanent building foundation support, MOLIT method) or additional (temporary
  tracked-plant platform, BR470 LSF method), or both in sequence. The method, load case, and
  acceptance criterion all depend on the answer.

---

## Stage 0 — Frame the zone

| | |
|---|---|
| **Sub-agent** | `/aggregate-platform` router, or `platform-design` |
| **PRD** | §1, §4.1, §5 Step 1; Appendix B |
| **Do** | Split the site into design zones (different subgrade, plant, or excavation proximity = separate zone). For each zone, fix the governing application and the governing load case. |
| **Output** | Zone list with application + load case per zone. Start a **design zone record** per Appendix B (`records/zone-records/<zone>-DRAFT.md`). |
| **Gate to Stage 1** | Application and governing load case confirmed for the zone. |

## Stage 1 — Design

| | |
|---|---|
| **Sub-agent** | `platform-design` (edge/slope screening may fan out to `platform-safety`) |
| **PRD** | §4.2–§4.4, §5 Steps 1–8, §7.1 |
| **Do** | Characterize subgrade (characteristic — cautious — Cu/CBR per zone). Select aggregate grading and decide if a geocell (하이셀/구속셀) layer is needed. Size platform thickness: <br>• **Primary application** — qa = qu ÷ 3 (lowest of Terzaghi/Meyerhof/empirical; Meyerhof-only for 하이셀/구속셀) ≥ applied pressure, **and** settlement (larger of Schmertmann/elastic) ≤ project limit (typ. 25.4 mm). <br>• **Additional application** — iterate thickness until LSF ≥ target (1.0 abs. min / 1.25 rigs & cranes / 1.5 soft or excavation-edge). <br>Check edge distance and slope stability (never from bearing capacity alone). Set surface falls (2–3%) and drainage. |
| **Output** | Design drawings (thickness by zone, geocell extents/laps, falls, edge distances, exclusion zones) + design basis report. Design zone record fields 1–7 populated. **Construction-stage verification requirements and hold points defined** (§5 Step 9). |
| **Gate to Stage 2** | Design issued and approved by the responsible engineer. Any subgrade-weaker-than-assumed contingency procedure documented. Open items (e.g. missing Cu-with-depth profile, plant pad geometry) closed. |

## Stage 2 — Construction

Run per zone, in this order. Each numbered step is a PRD §6 step; do not start one until the
previous step is signed off.

| Step | Sub-agent | PRD | Acceptance criterion (PRD §8) |
|---|---|---|---|
| **2.1 Pre-construction survey & clearance** | `platform-construction` (+ `site-safety` for exclusion zones, access routes, plant mobilization) | §6.1, §7.2 | Utilities located/protected; ground levels surveyed; exclusion zones and access established before plant arrives. |
| **2.2 Subgrade preparation & verification** | `platform-construction`; **`platform-safety` immediately if subgrade is below design** | §6.2, §7.2 | Proof roll 100% of footprint — no visible rutting/pumping/deflection. DCP or plate load test ≥ design characteristic Cu/CBR (min. 1 per zone, 1 per 200–500 m²). **Hold point** — no plant on the footprint until this is formally accepted. |
| **2.3 Geosynthetic (하이셀/구속셀) installation** *(if specified)* | `platform-construction` | §6.3 | Delivered product matches spec (certificate on file); correct orientation; overlaps ≥ specified; no tears; covered within the certified time (typ. same shift). |
| **2.4 Aggregate placement & compaction** | `platform-construction` | §6.4 | Lifts ≤ 300 mm compacted (company hard ceiling; 150–300 mm loose is the working assumption). Each lift ≥ 95% max dry density (Modified Proctor / KS F 2312) **before** the next lift. Inspect every lift for compaction, thickness, level before covering. |
| **2.5 Surface finishing & drainage** | `platform-construction` (+ `site-safety` for edge protection/signage) | §6.5, §7.3 | Trimmed to design falls (±0.5% of design fall); perimeter drainage discharging to an approved point **not into the excavation**; edge protection/barriers/signage in place before opening to traffic. |
| **2.6 Proof-load / trial-pass test** *(critical platforms — piling rigs, cranes)* | `platform-qaqc` (+ `platform-safety` for exclusion-zone conditions) | §6.6, §7.2 | Representative plant, critical locations, essential personnel only — no excessive rutting/deflection/distress. Engineer sign-off recorded. |
| **2.7 Handover** | `platform-qaqc` | §6.7 | As-built records compiled; **platform handover certificate** issued stating fitness for design loads and use restrictions (max outrigger load, excluded zones, max travel speed). Use envelope communicated to all operators and the temporary works coordinator before use. |

**Records produced:** as-built by zone, compaction/test results, geosynthetic install records,
proof-test results, handover certificate. Non-conformances → `records/nonconformance/`;
remedial work → `records/reinstatement/`.

## Stage 3 — Safety (runs across all stages, not after them)

| | |
|---|---|
| **Sub-agent** | `platform-safety` (platform structural/geotechnical hazards) · `site-safety` (daily briefings, PPE, plant, general site hazards) |
| **PRD** | §7.1 design · §7.2 construction · §7.3 in-service · §10 risk register |
| **Do** | Design stage: edge distance, higher LSF band for safety-critical platforms, worst-credible subgrade, mandatory hold points. Construction: exclusion zones, banksmen near the edge, no trafficking exposed geosynthetic, drainage maintained. In-service: display use envelope, visual inspection ≥ daily during active piling/crane ops, re-verify after heavy rain / freeze-thaw / extended standing load, monitor the excavation crest for tension cracks/bulging → stop plant in that zone and notify. |
| **Output** | Risk assessment mapped to the PRD §10 register; toolbox talks / daily safety documents (`app_pages/daily_safety.py` in the dashboard); stop-work notices. |

## Stage 4 — In-service, maintenance & decommissioning

| | |
|---|---|
| **Sub-agent** | `platform-qaqc` (monitoring, maintenance, decommissioning) · `platform-safety` (any hazard trend) |
| **PRD** | §7.3, §9 |
| **Do** | Routine visual inspection at frequency proportional to use (min. daily during active use, weekly otherwise). Level survey matched to settlement trend and criticality. Reinstate rutting by removing disturbed material and re-compacting in lifts + re-testing — **never** blade/regrade without compaction. Reassess design before any change of plant type/load/position. No excavation through the platform without a permit-to-work. At end of life: remove aggregate (and geosynthetic unless left by design — record its extent), reinstate, archive all QA/QC and monitoring records in the temporary works close-out file. |
| **Output** | Inspection/monitoring log; reinstatement records; decommissioning and close-out file. |

---

## Records map

Draft records are written under `records/<category>/*.md` (also creatable via the Streamlit
dashboard's "초안 저장"). Categories in use:

| Category | Path | Produced at |
|---|---|---|
| Design zone record (Appendix B) | `records/zone-records/` | Stage 0–1, finalized at Stage 2.7 |
| Non-conformance | `records/nonconformance/` | Any stage, on a failed check or discovered hazard |
| Reinstatement / retest | `records/reinstatement/` | After remedial work |

> **Durability caveat:** records saved through the *deployed* Streamlit app are **not durable**
> — the container filesystem is ephemeral, so a redeploy/restart/sleep wipes anything not
> committed to git. Commit records you need to keep. (Known, accepted limitation — see
> `CLAUDE.md`.)

## Every draft record carries a status banner

Sub-agents compile drafts marked **DRAFT — PENDING RESPONSIBLE ENGINEER'S REVIEW AND
SIGN-OFF**, with incomplete fields marked **PENDING**. A draft is not an approved design,
and no plant is positioned or mobilized on a zone until its record is reissued with the
responsible engineer's signature per PRD §6 Step 7 / §8.

## Knowledge base (sub-agents read these; so can you)

- `knowledge/aggregate-working-platform-prd.md` — full PRD, structured for read/grep
- `knowledge/company-specs-summary.md` — real 특별시방서 (페블테크/하이셀/조립골재/구속셀); hard
  specs that refine the PRD's generic figures
- `knowledge/design-worked-examples.md` — real project 검토서/계산서 examples
- `knowledge/field-video-notes.md` — field/product video review (250 mm field lift target,
  plate-load-test record example)
