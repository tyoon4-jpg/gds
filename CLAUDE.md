# gds — Aggregate Working Platform agentic program

This repo hosts an agentic AI program for site engineers working on the **Aggregate Working
Platform (페블테크/하이셀) system** — temporary aggregate/geocell platforms supporting tracked

## What's here

- `Aggregate_Working_Platform_PRD.docx` — the governing requirements document (design,
  construction, safety, QA/QC). Note: despite the extension this is a plain UTF-8 text file, not
  a real Word binary; see `knowledge/aggregate-working-platform-prd.md` for a structured
  markdown mirror that agents actually read.
- `GDS_spec/` — real company product specifications (특별시방서 for 페블테크/하이셀/조립골재/
  구속셀/메가헬리컬파일) and real project design/review/calculation packages (검토서/계산서/
  시공계획서, PDF and Excel). This is the ground-truth reference material the PRD's Appendix C
  originally flagged as pending.
- `knowledge/` — markdown summaries of the above, written for the sub-agents to `Read`/`Grep`
  directly: `aggregate-working-platform-prd.md`, `company-specs-summary.md`,
  `design-worked-examples.md`, `field-video-notes.md`.
- `.claude/agents/` — five specialist sub-agents: `platform-design`, `platform-construction`,
  `platform-safety`, `site-safety`, `platform-qaqc`. See their frontmatter `description` for
  trigger phrases. `platform-safety` owns active *platform* hazards (structural/geotechnical);
  `site-safety` owns daily safety documents, personal safety, and construction equipment safety.
- `.claude/skills/aggregate-platform/` — `/aggregate-platform` entry-point skill that routes a
  site engineer's request to the right sub-agent(s).

## How to route a site engineer's question

When working in this repo, prefer delegating platform-related questions to the specialist
sub-agents above (via the `Agent` tool, `subagent_type` = the agent's name) rather than answering
from general knowledge — they're grounded in this project's actual PRD and product specs, which
have two distinct design applications with different default methods (primary: permanent
building foundation support, MOLIT method; additional: temporary tracked-plant platforms, BR470
LSF method — see `knowledge/company-specs-summary.md`). A site engineer can also invoke
`/aggregate-platform` directly as a router if it's unclear which specialist applies.

**Safety-first routing rule:** if a request describes or implies an active hazard (rutting,
ponding, cracking near an excavation crest, plant exceeding its stated load envelope, a failed
test, subgrade weaker than expected), route to `platform-safety` first regardless of what else
is being asked.

Questions clearly outside this program's scope (general MiPM structural design — soldier piles,
waler beams, struts/rakers — or the unrelated 메가헬리컬파일 deep-foundation product) should be
answered plainly or declined per PRD §1.2 (out of scope), not forced into one of the five
sub-agents.

## Working conventions

- Treat `Aggregate_Working_Platform_PRD.docx` as Rev. A baseline; the `knowledge/` files layer in
  the GDS reference-material findings (Rev. B grounding) inline, flagged where they refine or
  diverge from the PRD's generic figures. If asked to formally revise the PRD, do so in the
  `.docx` file (as plain text) and keep `knowledge/aggregate-working-platform-prd.md` in sync.
- `GDS_spec/시방서.zip` must be extracted before its PDFs can be read — see
  `knowledge/company-specs-summary.md` for the extraction command. The four `.mp4` files in
  `GDS_spec/` are field/product/marketing video clips from the same company
  (㈜지반디자인앤솔루션); reviewed visually (sample frames + burned-in on-screen text, no
  speech-to-text) — see `knowledge/field-video-notes.md` for findings, including the company's
  practical 250mm field lift-thickness target and a real plate-load-test record example.
- This PRD explicitly scopes out implementing calculation software (§1.2) — sub-agents walk
  engineers through the design procedure and do arithmetic on given/confirmed inputs, but should
  not be turned into a standalone calculator tool without the user asking for that explicitly.
