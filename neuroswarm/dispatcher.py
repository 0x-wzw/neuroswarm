"""
NEUROSWARM Dual-Phase Dispatcher

The core orchestrator that routes every task through two phases:
  Phase 1 (WHAT): Brain resolves intent → skill, complexity, context
  Phase 2 (HOW):  Swarm deliberates approach → council, fallback, consensus

Usage:
    from neuroswarm.dispatcher import NeuroSwarmDispatcher

    dispatcher = NeuroSwarmDispatcher()
    result = dispatcher.dispatch("design the API architecture")
    # Phase 1: resolve intent
    # Phase 2: deliberate approach (if COMPLEX)
"""

from neuroswarm.brain.resolver import resolve, COMPLEXITY_MODEL_ROUTING
from neuroswarm.brain.signal_detector import detect
from neuroswarm.brain.brain_first import brain_check
from neuroswarm.swarm.council import Council
from neuroswarm.swarm.pre_spawn import pre_spawn_check
from neuroswarm.swarm.refusal_routing import get_next_model
from neuroswarm.bridge.context_feed import feed_context


class NeuroSwarmDispatcher:
    """Dual-phase dispatch: Brain determines WHAT, Swarm deliberates HOW."""

    def __init__(self, council_seats: dict | None = None):
        """Initialize the dispatcher with optional council configuration.

        Args:
            council_seats: Optional override for dimension → model mapping.
                          Defaults to the standard 10-D configuration.
        """
        self.council = Council(seats=council_seats)

    def resolve_intent(self, query: str) -> dict:
        """Phase 1: Brain determines WHAT to do.

        Resolves the intent to a skill, complexity rating, and model suggestion.
        Checks memory for cached context.

        Args:
            query: Natural language intent string.

        Returns:
            Dict with skill, complexity, model, brain_context, and council_needed flag.
        """
        # Step 1: Resolve intent
        resolution = resolve(query)

        # Step 2: Check memory for cached context
        brain_result = brain_check(query)

        # Step 3: Detect signals (always-on)
        signals = detect(query)

        # Step 4: Assemble brain context
        result = {
            **resolution,
            "brain_context": {
                "memory_hit": brain_result.get("memory_check", {}).get("found", False),
                "memory_source": brain_result.get("recommendation", "UNKNOWN"),
                "signals": signals.get("summary", {}),
                "memory_actions": signals.get("memory_actions", {}),
            },
            "council_needed": resolution.get("council_deliberation", False),
        }

        return result

    def deliberate(self, brain_result: dict, context: str = "") -> dict:
        """Phase 2: Swarm deliberates HOW to do it.

        Takes the brain's resolution and runs it through council deliberation
        if needed. Simple tasks skip the council.

        Args:
            brain_result: Output from resolve_intent().
            context: Additional context string for the council.

        Returns:
            Dict with approach, council_verdict (if council ran), and fallback_chain.
        """
        complexity = brain_result.get("primary", {}).get("complexity", "SIMPLE")

        # Simple tasks don't need council
        if complexity in ("TRIVIAL", "SIMPLE"):
            return {
                "approach": "direct_execution",
                "council_verdict": None,
                "fallback_chain": self._get_fallback_chain(complexity),
                "brain_result": brain_result,
            }

        # Moderate tasks: quick council (2-3 seats)
        if complexity == "MODERATE":
            seats = ["D7_general", "D9_research"]
            verdict = self.council.deliberate(
                task=brain_result.get("query", ""),
                seats=seats,
                brain_context=brain_result.get("brain_context", {}),
                context=context,
            )
            return {
                "approach": "quick_council",
                "council_seats": seats,
                "council_verdict": verdict,
                "fallback_chain": self._get_fallback_chain(complexity),
                "brain_result": brain_result,
            }

        # Complex tasks: full council deliberation
        seats = ["D1_synthesis", "D2_deep_reason", "D5_strategy"]
        verdict = self.council.deliberate(
            task=brain_result.get("query", ""),
            seats=seats,
            brain_context=brain_result.get("brain_context", {}),
            context=context,
        )
        return {
            "approach": "full_council",
            "council_seats": seats,
            "council_verdict": verdict,
            "fallback_chain": self._get_fallback_chain(complexity),
            "brain_result": brain_result,
        }

    def dispatch(self, query: str, context: str = "") -> dict:
        """Full dual-phase dispatch: Brain determines WHAT, Swarm deliberates HOW.

        Args:
            query: Natural language intent string.
            context: Additional context for council deliberation.

        Returns:
            Complete dispatch result with both phases.
        """
        # Phase 1: WHAT
        brain_result = self.resolve_intent(query)

        # Phase 2: HOW
        swarm_result = self.deliberate(brain_result, context=context)

        # Feed context back to brain (for future memory)
        feed_context(query, brain_result, swarm_result)

        return {
            "query": query,
            "phase_1_what": brain_result,
            "phase_2_how": swarm_result,
        }

    @staticmethod
    def _get_fallback_chain(complexity: str) -> list[str]:
        """Get the model fallback chain for a complexity level."""
        from neuroswarm.swarm.refusal_routing import FALLBACK_CHAINS
        return FALLBACK_CHAINS.get(complexity.lower(), FALLBACK_CHAINS["moderate"])


def main():
    """CLI entry point for NEUROSWARM dispatcher."""
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python -m neuroswarm.dispatcher \"<intent query>\" [--json]", file=sys.stderr)
        print("Example: python -m neuroswarm.dispatcher \"debug the login error\"", file=sys.stderr)
        sys.exit(1)

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    json_output = "--json" in sys.argv
    query = " ".join(args)

    dispatcher = NeuroSwarmDispatcher()
    result = dispatcher.dispatch(query)

    if json_output:
        print(json.dumps(result, indent=2))
    else:
        # Human-readable output
        brain = result["phase_1_what"]
        swarm = result["phase_2_how"]

        print(f"🧠☠️ NEUROSWARM Dispatch: \"{query}\"")
        print()
        print(f"  Phase 1 (WHAT):")
        if brain.get("primary"):
            print(f"    Skill: {brain['primary']['skill']}")
            print(f"    Complexity: {brain['primary']['complexity']}")
            print(f"    Model: {brain['primary']['suggested_model']}")
        if brain.get("brain_context"):
            bc = brain["brain_context"]
            print(f"    Memory: {'HIT' if bc.get('memory_hit') else 'MISS'}")
            if bc.get("signals"):
                s = bc["signals"]
                print(f"    Signals: {s.get('total_signals', 0)} "
                      f"(🔴{s.get('high', 0)} 🟡{s.get('medium', 0)} ⚪{s.get('low', 0)})")
        print()
        print(f"  Phase 2 (HOW):")
        print(f"    Approach: {swarm['approach']}")
        if swarm.get("council_seats"):
            print(f"    Council seats: {', '.join(swarm['council_seats'])}")
        if swarm.get("council_verdict"):
            print(f"    Verdict: {swarm['council_verdict'].get('verdict', 'pending')[:100]}...")
        print(f"    Fallback chain: {' → '.join(swarm['fallback_chain'][:3])}")


if __name__ == "__main__":
    main()