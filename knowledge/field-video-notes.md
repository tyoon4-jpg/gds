# Field / Marketing Video Notes

The four `.mp4` clips in `GDS_spec/` (all KakaoTalk downloads, no captions/subtitles file) have
been reviewed by extracting sample frames (ffmpeg) and reading their burned-in Korean on-screen
text — the videos have voice narration/audio that was **not** transcribed (no speech-to-text was
run), so treat this as a visual/on-screen-text review, not a full transcript. All four are
produced by the same company seen elsewhere in `GDS_spec/`: **㈜지반디자인앤솔루션 (Jiban Design
& Solution, "지반D&S")** — Instagram handle `@GDSOL__`, site `지반보강.kr` — the same firm whose
PE-stamped calc packages are summarized in `design-worked-examples.md`.

If a more precise figure or the audio narration is needed, re-extract frames at a finer interval
or run speech-to-text on the audio track directly from the source files.

## 1. `KakaoTalk_20260821_112148204.mp4` (2:10, 1280x720) — "하이셀 기초공법" (Hi-Cell Foundation Method)

Company training/promotional video, numbered installation stages (a "3단계" / Stage 3 title card
was captured showing geocell placement into an excavated, geotextile-lined pit with two workers
manually laying/pinning the honeycomb cells). Other captured stages: **원지반 다짐** (original
ground/subgrade compaction, roller shown) and **골재 다짐 및 편탄화** (aggregate compaction and
leveling — a roller compacting placed aggregate, on-screen text "완벽한 수평 평탄화를 완성합니다"
/ "achieves perfect horizontal leveling", and "시공면의 평탄성을 확보하고 기초 지반의 밀도를..."
/ "secures surface flatness and [original ground] density..."). Sequence visually matches the
company spec's install order in `company-specs-summary.md` (anchor pins → unroll → align → pin
interior → key/wire-tie overlaps) and the PRD §6 Step 2-3-4 order (subgrade compaction →
geosynthetic → aggregate placement/compaction). No new numeric specs beyond what's already
captured; useful as a visual training aid to point a site engineer to if they want to *see* the
sequence rather than read it.

## 2. `KakaoTalk_20260821_112154576.mp4` (1:05, 1280x720) — "PEBBLE TECH 시공사례 | 현장" (Pebble-Tech Construction Case Study | Site)

Real project site footage, titled sequence: **원지반다짐 → PET MAT 설치 → 골재반입 → 골재포설 →
시공완료** (subgrade compaction → PET MAT installation → aggregate delivery → aggregate placement
→ construction complete). Two findings that refine the numbers already in
`company-specs-summary.md`:

- **PET MAT** is the company's specific product name for the geotextile mat referenced elsewhere
  as "optional geotextile mat, design strength ≥50 kN/m" in the 페블테크 특별시방서 — shown here
  as a white woven sheet laid directly on the compacted subgrade before aggregate placement, i.e.
  this confirms PET MAT = the geotextile separation layer, not the geocell (하이셀/구속셀), for
  the aggregate-only Pebble-Tech product.
- **Practical compaction lift figure, more precise than the spec's ≤300mm ceiling:** on-screen
  text states *"최적의 지지력 확보를 위해 250mm 마다 층다짐 공정 반복"* — "to secure optimal
  bearing capacity, the layer-compaction process is repeated every 250mm" — alongside "맞물림
  저항력 증가" (increased interlocking resistance). **Treat 250mm as this company's actual
  practical target lift thickness in the field, within the 특별시방서's ≤300mm hard ceiling** —
  useful as the number to expect/verify on site rather than assuming the full 300mm every time.
- **Aggregate blend fractions used by the company's mixing equipment:** on-screen text states
  *"13, 19, 25, 40mm의 쇄석 골재를 현장 여건에 적합하게 배합 설계"* — "13, 19, 25, 40mm crushed
  stone aggregates are blended to a mix design suited to site conditions," using the "특수
  배합장비" (special blending equipment) shown — see video 3 below. This is the practical input
  gradation the on-site Pebble Mixer blends *from*, to hit the grading envelope in
  `company-specs-summary.md` (Dmax≤100mm, fines rules, Dmax/D80≥3, Cg 0.7–1.3, Cu 1.7–5).
- **A real, filled-in plate load test (평판재하시험) record is shown at "시공완료" (construction
  complete):**
  - Project: "...대성 전북 신공장 신축공사" (partial name visible — a 전북 [Jeonbuk] new factory
    construction project for a "...대성" company — likely a different/additional project from the
    five in `design-worked-examples.md`, not confirmed to be the same).
  - Test date: 2025년 6월 2일.
  - 설계하중 (design load): **250.0 kN/m²**.
  - 위치 (location): 현장내 No.7 (site location No. 7).
  - 기초폭 (foundation width/type): MAT.
  - 설계하중 재하판 침하량 (settlement at design load): **1.81 mm**.
  - 시험하중 재하판 침하량 (settlement at max test load): **8.00 mm at 792.6 kN/m²**.
  - 시험 최대하중 (max test load): **792.6 kN/m²** (test taken to ~3.2× design load).
  - **허용지지력 (allowable bearing capacity): 264.2 kN/m² 이상 — explicitly annotated "시험
    최대 하중의 1/3"** (= max test load ÷ 3). **This is a real, field-confirmed example of the
    FS=3.0-on-ultimate convention already documented in `design-worked-examples.md` §A.1** (there
    derived from the qa1 = qu/3 formula) — here it's the same 1/3 factor applied directly to the
    plate load test's max applied pressure rather than to a calculated qu, which is the standard
    KS F 2444 allowable-from-test-load convention. Useful as a template for what a completed,
    signed-off plate load test record should look like for a QA/QC handover package.

## 3. `KakaoTalk_20260821_112204354.mp4` (1:31, 1280x720) — "PEBBLE MIXER 페블믹서" (Pebble Mixer) Equipment Operation Manual

An operator training video for the **페블믹서 (Pebble Mixer)** — the company's proprietary
on-site "골재 특수배합장비" (special aggregate blending equipment) used to blend delivered
crushed-stone fractions (13/19/25/40mm, per video 2 above) into the Pebble-Tech/조립골재 grading
envelope on site, rather than requiring pre-blended aggregate to be trucked in. Numbered steps
captured on screen include: **Step 2 — 배합비 산출 (mix ratio calculation): "현장 맞춤형 최적
배합비"** (site-customized optimal mix ratio); **Step 5 — 장비 운용** (equipment operation);
**Step 8 — 장비 가동[연속]: 혼합 → 컨베이어1/2 → 토출** (continuous operation: mixing → conveyor
1/2 → discharge). The video closes with a photo-grid portfolio of multiple real project sites
using the finished product (soldier-pile-braced excavations with compacted aggregate platforms,
consistent with the MiPM/PRD context) — evidence of the product's field track record, not new
numeric spec content. **Practical implication for `platform-construction`:** if a site asks how
graded aggregate is being produced/blended on site rather than delivered pre-graded, this is the
equipment — worth mentioning as an option when discussing aggregate sourcing/logistics.

## 4. `KakaoTalk_20260821_112208234.mp4` (0:28, 406x720, vertical) — "페블텍 투수기층" (Pebble-Tech Permeable Base Layer) — social/marketing clip

Short vertical marketing clip (Instagram-style), not a technical/installation video. Headline:
*"투수블록 + 투수기층, 지반침하 대비 어떻게?"* ("Permeable block + permeable base layer — how to
prepare for ground settlement?"), branded "페블텍 투수기층" (Pebble-Tech permeable base layer),
with a call-to-action "투수 실험 보러가기" (go see the permeability test) and closing on the
company's Instagram handle `@GDSOL__ 지반디자인앤솔루션`.

**One substantive point worth carrying forward:** this clip frames Pebble-Tech partly around
**permeability/drainage performance** ("투수" = water-permeable), not just bearing capacity —
consistent with it being an unbound, open-graded crushed aggregate layer. Neither the PRD nor the
특별시방서 documents reviewed elsewhere quote a specific permeability coefficient — if a site
engineer asks about the platform's drainage/permeability performance specifically (e.g. for a
combined structural + stormwater-management use), that number isn't in this repo's knowledge base
yet and would need to be requested from the company's product datasheet or the "투수 실험"
(permeability test) referenced in this clip.

## Summary of new information for the design/construction/QA-QC agents

- **250mm** is the company's practical field lift-thickness target for Pebble-Tech compaction
  (within the 특별시방서's ≤300mm ceiling) — cite this as the expected figure, not just "up to
  300mm."
- **PET MAT** = the company's product name for the ≥50kN/m geotextile separation mat used under
  aggregate-only Pebble-Tech platforms.
- **13/19/25/40mm** crushed-stone input fractions are blended on-site (Pebble Mixer equipment) to
  hit the grading envelope, when aggregate isn't delivered pre-graded.
- A real plate load test record example confirms the **allowable bearing capacity = max test
  load ÷ 3** convention in practice (264.2 kN/m² allowable from 792.6 kN/m² max test load, KS F
  2444) — usable as a template for what a completed QA/QC handover test record should contain.
- Pebble-Tech is also marketed on **permeability/drainage** grounds — flag to the requester that
  no specific permeability coefficient is in this repo's knowledge base if that becomes relevant.
