"""Context Feed — Bridges Brain context into Swarm deliberation.

The bridge is where WHAT meets HOW. Brain context (memory hits, signals,
entity enrichment) gets packaged and fed into council deliberation prompts
so the swarm doesn't deliberate from scratch — it deliberates from knowledge.

Usage:
    from neuroswarm.bridge.context_feed import feed_context

    # After Phase 1 (Brain) completes, feed context to Phase 2 (Swarm)
    feed_context(query, brain_result, swarm_result)

    # Build a deliberation prompt with brain context
    prompt = build_deliberation_prompt(task, brain_context)
"""

from __future__ import annotations

from typing import Any


def feed_context(
    query: str,
    brain_result: dict[str, Any],
    swarm_result: dict[str, Any],
) -> dict[str, Any]:
    """Feed brain context into swarm and store the combined result.

    This is called after both phases complete. It packages the brain's
    findings (memory hits, signals, enrichment) so future deliberations
    can start from knowledge, not from zero.

    Args:
        query: The original intent string.
        brain_result: Output from Phase 1 (resolve_intent).
        swarm_result: Output from Phase 2 (deliberate).

    Returns:
        Combined context dict for storage/return.
    """
    context = {
        "query": query,
        "brain": {
            "skill": brain_result.get("primary", {}).get("skill"),
            "complexity": brain_result.get("primary", {}).get("complexity"),
            "model": brain_result.get("primary", {}).get("suggested_model"),
            "memory_hit": brain_result.get("brain_context", {}).get("memory_hit", False),
            "memory_source": brain_result.get("brain_context", {}).get("memory_source", "UNKNOWN"),
            "signals": brain_result.get("brain_context", {}).get("signals", {}),
            "memory_actions": brain_result.get("brain_context", {}).get("memory_actions", {}),
        },
        "swarm": {
            "approach": swarm_result.get("approach"),
            "council_seats": swarm_result.get("council_seats"),
            "fallback_chain": swarm_result.get("fallback_chain", [])[:3],  # Top 3 only
        },
    }

    return context


def build_deliberation_prompt(
    task: str,
    brain_context: dict[str, Any],
) -> str:
    """Build a council deliberation prompt enriched with brain context.

    This is the key innovation: the swarm doesn't deliberate from scratch.
    It deliberates with the brain's knowledge already loaded.

    Args:
        task: The task description for the council.
        brain_context: Brain context from Phase 1.

    Returns:
        Formatted prompt string with brain context injected.
    """
    sections = []

    # Task header
    sections.append(f"## Task\n{task}\n")

    # Memory context (if hit)
    if brain_context.get("memory_hit"):
        sections.append(
            "## Prior Knowledge (from memory)\n"
            f"Source: {brain_context.get('memory_source', 'unknown')}\n"
        )
    else:
        sections.append("## Prior Knowledge\nNo prior context found. Deliberate from first principles.\n")

    # Signals (always-on)
    signals = brain_context.get("signals", {})
    if signals:
        total = signals.get("total_signals", 0)
        high = signals.get("high", 0)
        sections.append(
            f"## Detected Signals\n"
            f"{total} signals detected "
            f"(🔴 {high} HIGH, 🟡 {signals.get('medium', 0)} MEDIUM, "
            f"⚪ {signals.get('low', 0)} LOW)\n"
        )

    # Memory actions (save recommendations)
    actions = brain_context.get("memory_actions", {})
    if actions.get("save_now"):
        sections.append(
            "## Memory Save Recommendations\n"
            + "\n".join(f"- {s}" for s in actions["save_now"])
            + "\n"
        )

    return "\n".join(sections)