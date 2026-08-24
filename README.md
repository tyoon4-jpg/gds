# gds — Aggregate Working Platform Agentic Program

An agentic AI program for **site engineers** working on the 페블테크 (Pebble-Tech) / 하이셀
(Hi-Cell) Aggregate Working Platform system — engineered aggregate (optionally geocell-
reinforced) layers used to improve ground bearing capacity, sized and verified through a
design → construction → safety → QA/QC workflow.

## What's in this repo

| Path | Contents |
|---|---|
| `Aggregate_Working_Platform_PRD.docx` | Governing requirements document (design method, step-by-step design & construction procedures, safety measures, QA/QC, risk register). Plain text despite the extension. |
| `GDS_spec/` | Real company product specifications (특별시방서) and real project design/review/calculation packages (검토서/계산서/시공계획서) — the ground-truth reference material. |
| `knowledge/` | Markdown summaries of the above, written for the sub-agents to read directly. |
| `.claude/agents/` | Four specialist sub-agents: **design**, **construction**, **safety**, **QA/QC**. |
| `.claude/skills/aggregate-platform/` | `/aggregate-platform` — entry-point router to the right sub-agent(s). |

## The four specialists

- **`platform-design`** — thickness sizing, bearing-capacity/settlement checks, geosynthetic/
  geocell selection, edge distance & slope stability screening.
- **`platform-construction`** — field sequencing: subgrade prep, geocell/geotextile
  installation, lift/compaction procedure, proof-load testing, handover.
- **`platform-safety`** — active hazards, exclusion zones, stop-work decisions, in-service
  inspection/monitoring, risk register.
- **`platform-qaqc`** — test frequency/acceptance criteria, product certificates, ITPs,
  as-built/handover records, maintenance/monitoring/decommissioning.

Open this project in Claude Code and either ask a question directly (the right specialist is
picked automatically) or run `/aggregate-platform` if you're not sure which one applies.

## Two applications, one system

The **primary application** of this system is **permanent building foundation support** — ground
improvement beneath mat foundations, slab-on-grade, and footings — sized with the company's
in-house MOLIT Terzaghi/Meyerhof/empirical + Schmertmann/elastic method (KCS 11 30 10). Every real
project reference file in `GDS_spec/` is this application. The **additional application** is
**temporary tracked-plant working platforms** (piling rigs, cranes, excavators during MiPM
excavation), sized to BR470/TWf's LSF method instead. Both use the same physical system and
company products — but different design load types, methods, and acceptance criteria. See
`knowledge/company-specs-summary.md`; the agents know to ask which application you mean before
quoting a number.

## Status

PRD is DRAFT Rev. A. The `knowledge/` files layer in findings from the real reference material
(what the PRD's Appendix C originally flagged as pending) — read those alongside the PRD, not
instead of it.
