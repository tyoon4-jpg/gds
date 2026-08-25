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
        "label": "Design",
        "icon": ":material/design_services:",
        "agent_file": ".claude/agents/platform-design.md",
        "blurb": "Thickness sizing, bearing capacity/settlement/LSF calcs, geosynthetic selection.",
    },
    "platform-construction": {
        "label": "Construction",
        "icon": ":material/construction:",
        "agent_file": ".claude/agents/platform-construction.md",
        "blurb": "Field sequencing: subgrade prep, installation, compaction, handover.",
    },
    "platform-safety": {
        "label": "Safety",
        "icon": ":material/health_and_safety:",
        "agent_file": ".claude/agents/platform-safety.md",
        "blurb": "Active platform hazards, exclusion zones, stop-work, in-service monitoring.",
    },
    "site-safety": {
        "label": "Site Safety",
        "icon": ":material/shield_person:",
        "agent_file": ".claude/agents/site-safety.md",
        "blurb": "Daily safety documents, PPE, general site hazards, equipment safety.",
    },
    "platform-qaqc": {
        "label": "QA / QC",
        "icon": ":material/fact_check:",
        "agent_file": ".claude/agents/platform-qaqc.md",
        "blurb": "Test frequency/acceptance criteria, ITPs, records, maintenance.",
    },
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
