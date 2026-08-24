"""Lightweight keyword-based router, mirroring the /aggregate-platform skill's rules:
safety-first on hazard language, otherwise score against each specialist's trigger phrases.

This is a heuristic, not an LLM call — kept fast and free. It intentionally errs toward
including a specialist rather than excluding one; the chat UI shows which were consulted.
"""

from __future__ import annotations

HAZARD_KEYWORDS = [
    "rutting", "rut ", "ponding", "standing water", "crack", "collapse", "collapsed",
    "tip over", "tipping", "unstable", "instability", "failed test", "exceeding",
    "exceeded", "soft spot", "subgrade weaker", "weaker than", "settlement observed",
    "settling", "bulging", "tension crack", "slip", "sinking", "punching through",
]

AGENT_KEYWORDS = {
    "platform-design": [
        "thickness", "bearing capacity", "bearing pressure", "lsf", "settlement",
        "geosynthetic", "geocell", "하이셀", "구속셀", "edge distance", "slope stability",
        "design zone", "friction angle", "meyerhof", "terzaghi", "how thick", "size the",
        "will it hold", "crane platform", "outrigger",
    ],
    "platform-construction": [
        "install", "lift thickness", "compaction", "compact", "proof roll", "subgrade prep",
        "next step", "handover", "as-built", "sequence", "what do i do", "field",
        "geocell installation", "aggregate placement", "pebble mixer",
    ],
    "platform-safety": [
        "safe", "safety", "hazard", "exclusion zone", "stop work", "risk", "incident",
        "notify", "crest", "excavation edge", "monitor", "inspection frequency",
    ],
    "platform-qaqc": [
        "test frequency", "acceptance criterion", "acceptance criteria", "itp",
        "certificate", "record", "maintenance", "decommission", "plate load",
        "how often do we test", "documentation", "nonconformance",
    ],
}

DEFAULT_AGENT = "platform-design"


def is_hazard(question: str) -> bool:
    q = question.lower()
    return any(kw in q for kw in HAZARD_KEYWORDS)


def route(question: str) -> list[str]:
    """Return an ordered list of agent keys to consult for this question.
    Safety-first: any hazard keyword puts platform-safety first, regardless of score."""
    q = question.lower()

    hazard_hit = any(kw in q for kw in HAZARD_KEYWORDS)

    scores: dict[str, int] = {}
    for agent_key, keywords in AGENT_KEYWORDS.items():
        scores[agent_key] = sum(1 for kw in keywords if kw in q)

    scored_agents = [a for a, s in scores.items() if s > 0]
    scored_agents.sort(key=lambda a: scores[a], reverse=True)

    if hazard_hit:
        ordered = ["platform-safety"] + [a for a in scored_agents if a != "platform-safety"]
        return ordered[:3] if len(ordered) > 3 else ordered

    if not scored_agents:
        return [DEFAULT_AGENT]

    return scored_agents[:2]
