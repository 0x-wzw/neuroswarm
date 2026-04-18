"""
NEUROSWARM Swarm — Pre-Spawn Analysis

Before spawning sub-agents, answer three questions in 10 seconds:
  Q1: Complexity? → Simple (don't spawn) / Complex → Q2
  Q2: Parallel seams? → No (don't spawn) / Yes → Q3
  Q3: Token math? → Spawn cost > expected output (don't spawn) / Sufficient → SPAWN

This is the swarm's gate for determining WHETHER to deliberate at all.
The brain resolves WHAT to do. Pre-spawn determines IF we need help.
"""

from dataclasses import dataclass
from enum import Enum


class Complexity(Enum):
    SIMPLE = "simple"
    SEMI_COMPLEX = "semi_complex"
    ULTRA_COMPLEX = "ultra_complex"


class Parallelism(Enum):
    SERIAL = "serial"
    PARALLEL = "parallel"


@dataclass
class SpawnDecision:
    """Result of pre-spawn analysis."""
    should_spawn: bool
    complexity: Complexity
    parallelism: Parallelism
    token_math: bool  # True if spawn cost < expected output
    reason: str
    recommended_seats: list[str]


# Spawn cost estimates (tokens)
SPAWN_OVERHEAD_MIN = 500
SPAWN_OVERHEAD_MAX = 1500
OUTPUT_MINIMUM_MULTIPLIER = 3  # Only spawn if expected output is 3-5x overhead


def pre_spawn_check(
    task_description: str,
    complexity: Complexity = Complexity.SIMPLE,
    has_parallel_seams: bool = False,
    expected_output_tokens: int = 0,
) -> SpawnDecision:
    """Run the 3-question pre-spawn gate.

    The swarm's gate for determining WHETHER to involve the council.

    Args:
        task_description: What the task is.
        complexity: Assessed complexity (from RESOLVER).
        has_parallel_seams: Whether the task has independent subspaces.
        expected_output_tokens: Estimated output tokens.

    Returns:
        SpawnDecision with should_spawn, reason, and recommended seats.
    """
    # Q1: Complexity?
    if complexity == Complexity.SIMPLE:
        return SpawnDecision(
            should_spawn=False,
            complexity=complexity,
            parallelism=Parallelism.SERIAL,
            token_math=False,
            reason=f"Simple task — no spawn needed. Handle in main session.",
            recommended_seats=[],
        )

    # Q2: Parallel seams?
    if not has_parallel_seams:
        return SpawnDecision(
            should_spawn=False,
            complexity=complexity,
            parallelism=Parallelism.SERIAL,
            token_math=False,
            reason=f"Serial dependency — compounding latency risk. Don't spawn.",
            recommended_seats=[],
        )

    # Q3: Token math?
    spawn_cost = SPAWN_OVERHEAD_MAX
    minimum_output = spawn_cost * OUTPUT_MINIMUM_MULTIPLIER

    if expected_output_tokens < minimum_output:
        return SpawnDecision(
            should_spawn=False,
            complexity=complexity,
            parallelism=Parallelism.PARALLEL,
            token_math=False,
            reason=f"Token math doesn't work: spawn cost ~{spawn_cost} tokens, "
                    f"expected output ~{expected_output_tokens} tokens. "
                    f"Need {minimum_output}+ tokens to justify spawn.",
            recommended_seats=[],
        )

    # All checks pass — spawn
    seats = _recommend_seats(complexity)
    return SpawnDecision(
        should_spawn=True,
        complexity=complexity,
        parallelism=Parallelism.PARALLEL,
        token_math=True,
        reason=f"Spawn justified: {complexity.value} task with parallel seams "
                f"and sufficient token budget ({expected_output_tokens} expected).",
        recommended_seats=seats,
    )


def _recommend_seats(complexity: Complexity) -> list[str]:
    """Recommend council dimensions based on task complexity."""
    if complexity == Complexity.ULTRA_COMPLEX:
        return ["D1_synthesis", "D2_deep_reason", "D5_strategy", "D6_analysis"]
    elif complexity == Complexity.SEMI_COMPLEX:
        return ["D1_synthesis", "D7_general"]
    else:
        return ["D7_general"]