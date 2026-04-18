"""Sparring Mode — Humans challenge, agents drive. No approval bottlenecks.

In NecroSwarm's sparring model:
- The agent presents its reasoning and proposed action
- The human challenges assumptions OR approves
- No "Should I do X?" — only "I'm doing X because [reasoning]. Any gaps?"

This module provides sparring-format message construction and validation.
"""

from __future__ import annotations

from enum import Enum
from dataclasses import dataclass, field


class SparRole(str, Enum):
    """Roles in a sparring exchange."""
    AGENT = "agent"
    HUMAN = "human"


class SparType(str, Enum):
    """Types of sparring messages."""
    PROPOSAL = "proposal"        # Agent proposes action with reasoning
    CHALLENGE = "challenge"      # Human challenges an assumption
    CONFIRMATION = "confirmation"  # Human confirms, proceed
    REVISION = "revision"        # Agent revises based on challenge


@dataclass
class SparMessage:
    """A single message in a sparring exchange."""
    role: SparRole
    spar_type: SparType
    content: str
    reasoning: str = ""
    gaps_identified: list[str] = field(default_factory=list)


# Anti-pattern patterns to detect approval-seeking
APPROVAL_PATTERNS = [
    "should i",
    "do you want me to",
    "can i",
    "would you like",
    "is it okay if",
    "shall i",
    "do you think i should",
    "want me to",
]

# Proactive sparring patterns to replace approval-seeking
SPARRING_TEMPLATES = {
    "proposal": (
        "I'm {action} because {reasoning}.\n"
        "You see any gaps?"
    ),
    "challenge_prompt": (
        "Here's my plan: {plan}\n"
        "Reasoning: {reasoning}\n"
        "Challenge if you see assumptions I'm missing."
    ),
    "status_update": (
        "Doing {action}. {reasoning}\n"
        "Flag if you disagree."
    ),
}


def format_spar(
    action: str,
    reasoning: str,
    gaps: list[str] | None = None,
) -> SparMessage:
    """Format a proactive sparring message (not approval-seeking).

    Args:
        action: What you're doing.
        reasoning: Why you're doing it.
        gaps: Optional known gaps to surface.

    Returns:
        SparMessage with proper sparring format.
    """
    return SparMessage(
        role=SparRole.AGENT,
        spar_type=SparType.PROPOSAL,
        content=f"I'm {action} because {reasoning}.",
        reasoning=reasoning,
        gaps_identified=gaps or [],
    )


def detect_approval_seeking(message: str) -> bool:
    """Detect if a message is approval-seeking (anti-pattern).

    Args:
        message: The agent's proposed message to the human.

    Returns:
        True if the message is approval-seeking (bad), False if sparring (good).
    """
    lower = message.lower().strip()
    return any(pattern in lower for pattern in APPROVAL_PATTERNS)


def reframe_to_spar(approval_message: str) -> str:
    """Reframe an approval-seeking message into a sparring message.

    Args:
        approval_message: The approval-seeking message to reframe.

    Returns:
        A sparring-format message.
    """
    # Strip the approval pattern
    lower = approval_message.lower()

    if "should i" in lower:
        # "Should I deploy?" → "I'm deploying because [reasoning]."
        action = approval_message.replace("Should I", "I'm").replace("should i", "I'm")
        action = action.rstrip("?") + "."
        return action + " You see any gaps?"

    if "can i" in lower or "may i" in lower:
        action = approval_message.replace("Can I", "I will").replace("can I", "I will")
        action = action.replace("May I", "I will").replace("may I", "I will")
        action = action.rstrip("?") + "."
        return action + " Challenge if you disagree."

    # Default: just add sparring suffix
    return approval_message.rstrip("?.") + ". You see any gaps?"


def format_handoff(
    to_agent: str,
    task_type: str,
    content: str,
    approach: str,
    report_to: str = "Hermes",
) -> str:
    """Format a standard NecroSwarm handoff message.

    Args:
        to_agent: Name of the receiving agent.
        task_type: urgent, status_update, task_delegation, question, or data_pass.
        content: Task description.
        approach: Agreed approach.
        report_to: Who to report back to.

    Returns:
        Formatted handoff message.
    """
    return (
        f"TO: {to_agent}\n"
        f"TYPE: {task_type}\n"
        f"CONTENT: {content}\n"
        f"APPROACH: {approach}\n"
        f"REPORT_TO: {report_to}"
    )