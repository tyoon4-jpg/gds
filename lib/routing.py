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
    # Korean equivalents
    "러팅", "바퀴자국", "물고임", "침수", "균열", "붕괴", "전도", "불안정",
    "시험 실패", "시험불합격", "초과", "연약지반", "물렁", "노상 약화", "노상약화",
    "침하", "부풀음", "융기", "인장균열", "미끄러짐", "활동", "가라앉", "관입",
]

AGENT_KEYWORDS = {
    "platform-design": [
        "thickness", "bearing capacity", "bearing pressure", "lsf", "settlement",
        "geosynthetic", "geocell", "하이셀", "구속셀", "edge distance", "slope stability",
        "design zone", "friction angle", "meyerhof", "terzaghi", "how thick", "size the",
        "will it hold", "crane platform", "outrigger",
        # Korean equivalents
        "두께", "지지력", "베어링압력", "침하량", "지오신세틱", "지오셀", "이격거리",
        "사면안정", "설계존", "마찰각", "마이어호프", "테르자기", "얼마나 두껍", "크기산정",
        "견딜까", "크레인 플랫폼", "아웃트리거",
    ],
    "platform-construction": [
        "install", "lift thickness", "compaction", "compact", "proof roll", "subgrade prep",
        "next step", "handover", "as-built", "sequence", "what do i do", "field",
        "geocell installation", "aggregate placement", "pebble mixer",
        # Korean equivalents
        "설치", "다짐 층두께", "다짐", "포설", "프루프롤", "노상 준비", "노상준비",
        "다음 단계", "인수인계", "준공도면", "지오셀 설치", "골재 포설", "페블믹서",
    ],
    "platform-safety": [
        "safe", "safety", "hazard", "exclusion zone", "stop work", "risk", "incident",
        "notify", "crest", "excavation edge", "monitor", "inspection frequency",
        # Korean equivalents
        "안전", "위험", "배제구역", "작업중지", "리스크", "사고", "통보", "비탈머리",
        "굴착 경계", "모니터링", "점검주기",
    ],
    "site-safety": [
        "toolbox talk", "daily safety", "safety briefing", "ppe", "jsa",
        "job safety analysis", "heat stress", "cold stress", "manual handling",
        "pre-use check", "pre-use inspection", "equipment inspection", "muster point",
        "site induction", "near miss", "incident report", "housekeeping",
        "traffic management", "working at height",
        # Korean equivalents
        "일일안전", "일일 안전", "안전브리핑", "안전 브리핑", "작업전 안전점검회의", "tbm",
        "보호구", "위험성평가", "열사병", "한랭", "수작업", "장비점검", "장비 점검",
        "가동전 점검", "가동 전 점검", "장비 검사", "집결지", "현장 오리엔테이션",
        "아차사고", "사고보고", "사고 보고",
    ],
    "platform-qaqc": [
        "test frequency", "acceptance criterion", "acceptance criteria", "itp",
        "certificate", "record", "maintenance", "decommission", "plate load",
        "how often do we test", "documentation", "nonconformance",
        # Korean equivalents
        "시험빈도", "시험 빈도", "합격기준", "합격 기준", "검사기준서", "준공", "인증서",
        "다짐도", "시방서", "유지관리", "폐지", "평판재하시험", "얼마나 자주 시험",
        "부적합",
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
