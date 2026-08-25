---
name: aggregate-platform
description: >
  Entry point for the Aggregate Working Platform (페블테크/하이셀) agentic program. Use when a
  site engineer opens with a general request about the working platform — e.g. "help with the
  platform on site X", "I need to check something about 페블테크/하이셀", or when it's unclear
  which specialist (design/construction/safety/site-safety/QA-QC) applies. Routes to the right
  sub-agent(s) and can fan out to more than one when a request spans stages.
---

# Aggregate Working Platform — agentic program router

This project (`gds`) runs a five-specialist agentic program for the Aggregate Working Platform
(페블테크) system, grounded in `Aggregate_Working_Platform_PRD.docx` and the real product specs
and project calculation examples under `GDS_spec/` (mirrored for agent use in `knowledge/`).

The specialists, defined in `.claude/agents/`:

| Agent | Use for |
|---|---|
| `platform-design` | Thickness sizing, bearing capacity/settlement/LSF calcs, geosynthetic/geocell selection, edge distance & slope stability screening, drainage design |
| `platform-construction` | Field sequencing: subgrade prep, geosynthetic/geocell installation, lift/compaction procedure, surface finishing, proof-load testing, handover |
| `platform-safety` | Active platform hazards (rutting, ponding, cracking, overload), exclusion zones tied to platform monitoring, stop-work decisions, in-service inspection/monitoring, risk register |
| `site-safety` | Daily safety documents/toolbox talks, personal safety (PPE, manual handling, heat/cold stress), general site hazards (housekeeping, traffic, working at height), construction equipment safety (pre-use checks, exclusion zones around plant) |
| `platform-qaqc` | Test frequency/acceptance criteria, product certificates, ITPs, as-built/handover records, maintenance/monitoring/decommissioning |

## What to do when this skill is invoked

1. **Read the request and decide routing.** Most single-topic questions map cleanly to one
   agent — use the table above and each agent's `description` frontmatter (they contain trigger
   phrases). If genuinely ambiguous, ask one short clarifying question rather than guessing.
2. **Active platform hazard takes priority.** If the request describes or implies an in-progress
   hazard to the platform itself (rutting, ponding, a crack near the excavation crest, plant
   exceeding its load envelope, subgrade found weaker than expected, a proof roll/test that just
   failed) — route to `platform-safety` first, regardless of what else the request also asks
   about. Safety questions don't wait for a full design/construction answer. A request for a daily
   safety document/toolbox talk, PPE guidance, or equipment pre-use/exclusion-zone question
   (not tied to the platform's structural condition) routes to `site-safety` instead — it isn't an
   "active hazard" in the platform-safety sense, so don't force it through that priority path.
3. **Multi-stage requests fan out.** A request like "we found soft ground during subgrade prep,
   what do we do" spans construction (what step, what's the hold point) and safety (stop-work,
   notify) and possibly design (revised thickness) — call more than one sub-agent via the `Agent`
   tool if the request genuinely needs more than one specialist's answer, and present the
   combined result coherently rather than three disconnected blocks. A daily safety document often
   spans `site-safety` (personal safety, equipment, general hazards) and `platform-safety` (any
   platform-specific item of the day, e.g. a current exclusion zone) — fan out to both rather than
   letting `site-safety` invent a platform-hazard figure itself.
4. **Delegate via the `Agent` tool** with `subagent_type` set to the chosen agent name(s) from
   the table. Give each sub-agent the full original request plus any context already gathered in
   this conversation — sub-agents don't share your conversation history unless you include it.
5. **If the request is clearly none of the five** (e.g. general questions about the MiPM
   structural system, soldier piles, waler beams, struts/rakers themselves, or the unrelated
   메가헬리컬파일 deep-foundation product) — say so, note this program's scope is the Aggregate
   Working Platform specifically (PRD §1.2 lists what's out of scope), and answer briefly from
   general knowledge/the knowledge base if you can, without inventing a sub-agent that doesn't
   exist.

## Knowledge base (all four sub-agents read these; you can too)

- `knowledge/aggregate-working-platform-prd.md` — full PRD, structured for grep/read.
- `knowledge/company-specs-summary.md` — real product specs (페블테크/하이셀/조립골재/구속셀/
  메가헬리컬파일) extracted from `GDS_spec/시방서.zip`, including confirmation that this system
  has two applications (PRD §1): primary (permanent building foundation support, MOLIT
  Terzaghi/Meyerhof/empirical bearing + Schmertmann/elastic settlement method) and additional
  (temporary tracked-plant working platforms, the PRD's BR470/TWf LSF method).
- `knowledge/design-worked-examples.md` — real project calculation examples extracted from
  `GDS_spec/` review/calc reports and spreadsheets.
- `knowledge/field-video-notes.md` — visual review of the four `GDS_spec/*.mp4` training/site/
  marketing clips (frames + on-screen text; audio not transcribed).

If a knowledge file looks stale or a site engineer supplies a newer project document, read the
new source directly (PDF/xlsx under `GDS_spec/`, or whatever they provide) rather than trusting
a summary that may be out of date.
