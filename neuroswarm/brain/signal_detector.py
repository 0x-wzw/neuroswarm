"""
NEUROSWARM Brain — Signal Detection

Always-on ambient signal capture. Extracts entities, preferences, and patterns
from every message. Classifies each signal as HIGH/MEDIUM/LOW priority.

Evolved from GBrain's sub-agent spawn pattern into a local classification
module that doesn't require spawning a separate agent for simple cases.

The brain captures WHAT to remember. The swarm decides HOW to act on it.
"""

import re
from typing import Any

# ── Entity Patterns ─────────────────────────────────────────────────

ENTITY_PATTERNS = {
    "github_repo": re.compile(r'\b([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)\b'),
    "url": re.compile(r'https?://[^\s<>"{}|\\\^`\[\]]+'),
    "file_path": re.compile(r'(?:~?/[\w./-]+\.[\w]+)|(?:~?/[\w./-]+/[\w./-]*)'),
    "model_name": re.compile(r'\b(kimi-k2(?:\.5)?|deepseek-v3\.1|glm-5\.1|qwen3-coder|minimax-m2\.5|mistral-large-3|devstral-2|gemma[34]?|nemotron|ministral)\b', re.IGNORECASE),
    "tool_name": re.compile(r'\b(gh|himalaya|mcporter|git|docker|python|node|npm|curl)\b'),
    "project_name": re.compile(r'\b(VoidTether|NecroSwarm|NeuroSwarm|HyperFrames?|OpenClaw|Hermes|clawXiv|GBrain)\b', re.IGNORECASE),
    "tech_concept": re.compile(r'\b(JSON-RPC|MCP|A2A|LLM|RAG|FTS5|RRF|API|REST|gRPC|WebSocket)\b'),
}

# ── Preference Patterns ─────────────────────────────────────────────

PREFERENCE_PATTERNS = [
    (re.compile(r"(?:I prefer|I like|my preference|I'd rather)\s+(.+)", re.IGNORECASE), "preference"),
    (re.compile(r"(?:don't|do not|never|stop)\s+(?:ask|prompt|request)\s+(?:me\s+)?(?:for\s+)?(.+)", re.IGNORECASE), "correction"),
    (re.compile(r"(?:always|must|should|need to)\s+(.+)", re.IGNORECASE), "directive"),
    (re.compile(r"(?:that worked|that's perfect|great job|nice)\b", re.IGNORECASE), "praise"),
    (re.compile(r"(?:this keeps|keeps on|again|still)\s+(.+)", re.IGNORECASE), "frustration"),
    (re.compile(r"(?:actually|rather|instead)\s+(.+)", re.IGNORECASE), "correction"),
]

# ── Memory Decision Matrix ──────────────────────────────────────────

MEMORY_RULES = {
    "HIGH": {
        "patterns": ["preference", "correction", "directive"],
        "action": "SAVE immediately to memory",
    },
    "MEDIUM": {
        "patterns": ["praise", "entity_project", "entity_model"],
        "action": "SAVE to memory if durable, skip if transient",
    },
    "LOW": {
        "patterns": ["frustration", "entity_file", "entity_url"],
        "action": "SKIP — will resurface if important",
    },
}


def detect_entities(text: str) -> list[dict[str, Any]]:
    """Extract named entities from text."""
    entities = []
    seen = set()

    for entity_type, pattern in ENTITY_PATTERNS.items():
        for match in pattern.finditer(text):
            value = match.group(0)
            key = f"{entity_type}:{value}"
            if key not in seen:
                seen.add(key)
                entities.append({"type": entity_type, "value": value, "position": match.start()})

    return entities


def detect_preferences(text: str) -> list[dict[str, Any]]:
    """Extract preference and correction signals from text."""
    preferences = []

    for pattern, signal_type in PREFERENCE_PATTERNS:
        for match in pattern.finditer(text):
            captured = match.group(1) if match.lastindex else match.group(0)
            preferences.append({
                "type": signal_type,
                "text": match.group(0),
                "captured": captured,
                "position": match.start(),
            })

    return preferences


def classify_signals(entities: list[dict], preferences: list[dict]) -> list[dict[str, Any]]:
    """Classify all signals by memory priority."""
    signals = []

    for entity in entities:
        etype = entity["type"]
        priority = "MEDIUM" if etype in ("project_name", "model_name") else "LOW"
        signals.append({
            "kind": "entity",
            "type": etype,
            "value": entity["value"],
            "priority": priority,
            "memory_action": MEMORY_RULES[priority]["action"],
        })

    for pref in preferences:
        ptype = pref["type"]
        priority = "HIGH" if ptype in ("preference", "correction", "directive") else "MEDIUM" if ptype == "praise" else "LOW"
        save_suggestion = pref.get("captured", pref["text"]).strip().rstrip(".") if priority == "HIGH" else None
        signals.append({
            "kind": "preference",
            "type": ptype,
            "value": pref["text"],
            "priority": priority,
            "memory_action": MEMORY_RULES[priority]["action"],
            "save_suggestion": save_suggestion,
        })

    priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    signals.sort(key=lambda s: priority_order.get(s["priority"], 3))

    return signals


def detect(text: str) -> dict:
    """Run full signal detection on text.

    The brain's always-on scanner. Determines WHAT signals exist in a message.

    Args:
        text: Input message to analyze.

    Returns:
        Detection results with entities, preferences, signals, and memory actions.
    """
    entities = detect_entities(text)
    preferences = detect_preferences(text)
    signals = classify_signals(entities, preferences)

    high_signals = [s for s in signals if s["priority"] == "HIGH"]
    medium_signals = [s for s in signals if s["priority"] == "MEDIUM"]
    low_signals = [s for s in signals if s["priority"] == "LOW"]

    memory_saves = [s["save_suggestion"] for s in high_signals if s.get("save_suggestion")]

    return {
        "input": text,
        "entities": entities,
        "preferences": preferences,
        "signals": signals,
        "summary": {
            "total_signals": len(signals),
            "high": len(high_signals),
            "medium": len(medium_signals),
            "low": len(low_signals),
        },
        "memory_actions": {
            "save_now": memory_saves,
            "consider_saving": [s["value"] for s in medium_signals],
            "skip": [s["value"] for s in low_signals],
        },
    }