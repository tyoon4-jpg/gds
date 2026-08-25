"""Loads the agent instruction files and knowledge base for the dashboard app.

Mirrors the same sources the real Claude Code sub-agents read
(.claude/agents/*.md + knowledge/*.md), so the dashboard's answers stay
grounded in the same PRD/company-spec/worked-example material.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

AGENTS: dict[str, dict[str, str]] = {
    "platform-design": {
        "label": "설계",
        "icon": ":material/design_services:",
        "agent_file": ".claude/agents/platform-design.md",
        "blurb": "두께 산정, 지지력/침하/LSF 계산, 지오신세틱 선정.",
    },
    "platform-construction": {
        "label": "시공",
        "icon": ":material/construction:",
        "agent_file": ".claude/agents/platform-construction.md",
        "blurb": "현장 시공 순서: 노상 준비, 설치, 다짐, 인수인계.",
    },
    "platform-safety": {
        "label": "플랫폼 안전",
        "icon": ":material/health_and_safety:",
        "agent_file": ".claude/agents/platform-safety.md",
        "blurb": "플랫폼 관련 위험, 배제구역, 작업중지, 사용중 모니터링.",
    },
    "site-safety": {
        "label": "현장 안전",
        "icon": ":material/shield_person:",
        "agent_file": ".claude/agents/site-safety.md",
        "blurb": "일일 안전문서, 보호구(PPE), 일반 현장 위험, 장비 안전.",
    },
    "platform-qaqc": {
        "label": "품질(QA/QC)",
        "icon": ":material/fact_check:",
        "agent_file": ".claude/agents/platform-qaqc.md",
        "blurb": "시험 빈도/합격기준, 검사기준서(ITP), 기록, 유지관리.",
    },
}

CATEGORY_LABELS: dict[str, str] = {
    "zone-records": "구역별 기록",
    "nonconformance": "부적합 사항",
    "reinstatement": "복구 기록",
    "daily-safety": "일일 안전문서",
    "other": "기타",
}

KNOWLEDGE_FILES = [
    "knowledge/aggregate-working-platform-prd.md",
    "knowledge/company-specs-summary.md",
    "knowledge/design-worked-examples.md",
    "knowledge/field-video-notes.md",
]

RECORDS_DIR = REPO_ROOT / "records"
RECORD_CATEGORIES = ["zone-records", "nonconformance", "reinstatement", "daily-safety", "other"]

_DASHBOARD_LIMITATIONS = """
## Interface limitations (read before answering)

You are running inside a standalone Streamlit dashboard, not Claude Code. Important
differences from the full agentic program:

- You have **no live file access** — no Read/Grep/Bash tools. Everything you know is in this
  system prompt: your own agent instructions plus the four knowledge files below. You cannot
  open a specific PDF/xlsx under `GDS_spec/`, cannot read a specific draft under `records/`, and
  cannot check current git/file state.
- If a question needs something not included in this prompt (a specific reference document, a
  specific existing draft record, current repo state), **say so explicitly and recommend the
  site engineer use Claude Code directly against this repository** for that — do not guess or
  fabricate what such a file might contain.
- You cannot write files yourself. If your answer would normally end in drafting a record, give
  the content in your response — the dashboard has a separate "Save as draft record" action the
  user can use to write it to `records/`, but that's a UI action, not something you do.
- Stay in your own lane (see your role below). This dashboard shows other specialists as
  separate chat tabs — if a question is really theirs, say so, but still answer the part that's
  yours.

## Output language

The site engineers using this dashboard are Korean-speaking. **Always respond in Korean
(한국어)**, regardless of what language the question was asked in. Keep proper nouns, product
names, and standard technical notation as commonly used on Korean sites rather than translating
them: 페블테크, 하이셀, 구속셀, PET MAT, unit symbols (kPa, kN/m³, mm, m), formula/method names
(Terzaghi, Meyerhof, Schmertmann, LSF), and Greek symbols (φ, γ, ν). Numbers and formulas stay as
written.

**Marker words stay literally in English even inside Korean text**, because the dashboard's
Site status/Records pages scan the saved file for these exact tokens to compute badges and
counts — translating them would silently break that feature:
- `DRAFT` — any record you draft must include this exact word (e.g. "**상태: 초안(DRAFT)** — ...").
- `PENDING` — any field/item still open or awaiting confirmation must be marked with this exact
  word (e.g. "트랙 패드 폭/길이: **PENDING** — 장비 제원표에서 아직 확보되지 않음").
Write the surrounding sentence in Korean; just don't translate `DRAFT`/`PENDING` themselves.
"""


def _strip_frontmatter(text: str) -> str:
    """Strip a leading YAML frontmatter block (--- ... ---) from agent markdown files."""
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    return text[end + 4 :].lstrip("\n")


def _read(relative_path: str) -> str:
    path = REPO_ROOT / relative_path
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"[missing file: {relative_path}]"


def build_system_prompt(agent_key: str) -> str:
    """Assemble the full system prompt for one specialist: its own instructions +
    the shared knowledge base + a note about this interface's limitations."""
    agent = AGENTS[agent_key]
    instructions = _strip_frontmatter(_read(agent["agent_file"]))

    knowledge_sections = []
    for rel_path in KNOWLEDGE_FILES:
        content = _read(rel_path)
        knowledge_sections.append(f"### Source: `{rel_path}`\n\n{content}")
    knowledge_blob = "\n\n---\n\n".join(knowledge_sections)

    return (
        f"{instructions}\n\n"
        f"{_DASHBOARD_LIMITATIONS}\n\n"
        f"# Knowledge base (full text, read before answering)\n\n{knowledge_blob}"
    )
