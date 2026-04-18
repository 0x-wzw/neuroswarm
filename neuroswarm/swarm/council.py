"""
NEUROSWARM Swarm — 10-D Council Deliberation

The council is the second half of the dual-phase dispatch.
While the brain resolves WHAT to do, the council deliberates HOW.

Each dimension brings a different cognitive capability:
  D1  Synthesis    — Converge perspectives into coherent whole
  D2  Deep Reason  — Analyze deeply, find hidden implications
  D3  Code         — Generate, review, verify code
  D4  Vision       — See and interpret visual information
  D5  Strategy     — Plan strategically, weigh trade-offs
  D6  Analysis     — Break down complex systems quantitatively
  D7  General       — Fast general-purpose reasoning
  D8  Verification  — Fact-check, accuracy gate
  D9  Research      — Gather and synthesize information
  D10 Think        — Slow, thorough, second-order reasoning

The council receives brain context (memory hits, signals, enrichment)
and deliberates with full knowledge of what the brain already knows.
"""

from neuroswarm.swarm.dimension_map import DIMENSION_MAP, DIMENSION_FALLBACK


class Council:
    """10-D Council Deliberation Engine.

    The swarm deliberates HOW to execute, using brain context to inform
    its deliberation. This is the key innovation: brain context feeds
    into council deliberation, so models don't repeat work the brain
    already knows about.
    """

    def __init__(self, seats: dict | None = None):
        """Initialize council with optional custom dimension → model mapping.

        Args:
            seats: Optional override for dimension → model mapping.
                   Defaults to the standard 10-D configuration.
        """
        self.seats = seats or DIMENSION_MAP

    def deliberate(
        self,
        task: str,
        seats: list[str] | None = None,
        brain_context: dict | None = None,
        context: str = "",
    ) -> dict:
        """Run council deliberation on a task.

        Args:
            task: The task description (from brain's resolution).
            seats: Which dimensions to involve (e.g., ["D1_synthesis", "D7_general"]).
            brain_context: Context from the brain phase (memory hits, signals).
            context: Additional context string.

        Returns:
            Dict with verdict, consensus info, and context used.
        """
        if seats is None:
            seats = ["D1_synthesis", "D7_general"]

        # Build deliberation context
        deliberation_context = self._build_context(task, brain_context, context)

        # Determine models for each seat
        seat_models = {}
        for seat in seats:
            if seat in self.seats:
                seat_models[seat] = self.seats[seat]

        return {
            "task": task,
            "seats": seat_models,
            "context_used": deliberation_context,
            "brain_context_applied": brain_context is not None,
            "verdict": "pending",  # Actual deliberation happens via Ollama Cloud calls
            "approach": self._suggest_approach(seats, task, brain_context),
            "fallback_plan": self._build_fallback_plan(seats),
        }

    def _build_context(
        self,
        task: str,
        brain_context: dict | None,
        extra_context: str,
    ) -> str:
        """Build the full context for council deliberation.

        Includes brain context (what we already know) so the council
        doesn't repeat work that memory already has.
        """
        parts = [f"Task: {task}"]

        if brain_context:
            if brain_context.get("memory_hit"):
                parts.append("[BRAIN: Relevant context found in memory]")
            if brain_context.get("signals"):
                signals = brain_context["signals"]
                parts.append(f"[BRAIN: {signals.get('total_signals', 0)} signals detected]")

        if extra_context:
            parts.append(f"Context: {extra_context}")

        return "\n".join(parts)

    def _suggest_approach(
        self,
        seats: list[str],
        task: str,
        brain_context: dict | None,
    ) -> str:
        """Suggest an approach based on which dimensions are deliberating."""
        if "D1_synthesis" in seats and "D2_deep_reason" in seats:
            return "full_synthesis"
        elif "D1_synthesis" in seats:
            return "quick_synthesis"
        elif "D5_strategy" in seats:
            return "strategic_analysis"
        elif "D7_general" in seats:
            return "general_consensus"
        else:
            return "focused_review"

    def _build_fallback_plan(self, seats: list[str]) -> dict:
        """Build a fallback plan for each dimension in the council.

        If a dimension's model refuses or errors, route to the
        dimension's backup rather than a flat list.
        """
        fallback = {}
        for seat in seats:
            if seat in DIMENSION_FALLBACK:
                fallback[seat] = DIMENSION_FALLBACK[seat]
        return fallback