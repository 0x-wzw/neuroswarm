"""
NEUROSWARM Swarm — Refusal Routing

Dimension-aware model fallback chains. When a council model refuses or
errors, route to the NEXT MODEL IN THE SAME DIMENSION rather than a flat list.

GBrain's version: primary → DeepSeek → Qwen → Grover (flat)
NEUROSWARM's version: D7_general fails → D1_synthesis → D9_research (dimensional)

This is the key innovation: a flat fallback chain doesn't know which
dimension failed. NEUROSWARM preserves cognitive diversity by routing
to the dimension's backup model.
"""

from neuroswarm.swarm.dimension_map import DIMENSION_FALLBACK

# ── Refusal Detection ────────────────────────────────────────────────

REFUSAL_PATTERNS = [
    "i cannot", "i can't", "i'm unable", "i'm not able",
    "i apologize but", "as an ai", "as a language model",
    "i must decline", "against my guidelines", "not appropriate",
    "content policy", "i won't be able to", "i'm not going to",
    "i'm sorry, but i can't", "against my", "ethical guidelines",
    "harmful or",
]

DEAD_MODELS = ["qwen3.5:cloud"]  # Permanently dead, skip immediately

EMPTY_RESPONSE_THRESHOLD = 20  # Characters below this = suspiciously short


def is_refusal(response: str) -> bool:
    """Check if a model response is a refusal."""
    lower = response.strip().lower()
    if len(lower) < EMPTY_RESPONSE_THRESHOLD:
        return True
    return any(pattern in lower for pattern in REFUSAL_PATTERNS)


def classify_error(error_type: str, response: str = "") -> str:
    """Classify the type of failure.
    Returns: REFUSAL, TIMEOUT, EMPTY, ERROR, or DEAD_MODEL
    """
    if error_type == "dead_model":
        return "DEAD_MODEL"
    if error_type == "timeout":
        return "TIMEOUT"
    if error_type == "empty" or (response and len(response.strip()) < EMPTY_RESPONSE_THRESHOLD):
        return "EMPTY"
    if error_type == "error":
        return "ERROR"
    if response and is_refusal(response):
        return "REFUSAL"
    return "UNKNOWN"


# ── Fallback Chains ──────────────────────────────────────────────────

FALLBACK_CHAINS = {
    "complex": [
        "kimi-k2.5:cloud",
        "deepseek-v3.1:671b:cloud",
        "glm-5.1:cloud",
        "devstral-2:123b:cloud",
    ],
    "moderate": [
        "minimax-m2.5:cloud",
        "mistral-large-3:675b:cloud",
        "glm-5.1:cloud",
    ],
    "simple": [
        "gemma3:27b:cloud",
        "glm-5.1:cloud",
        "ministral-3:3b:cloud",
    ],
    "code": [
        "qwen3-coder:480b:cloud",
        "deepseek-v3.1:671b:cloud",
        "devstral-2:123b:cloud",
    ],
    "research": [
        "minimax-m2.5:cloud",
        "kimi-k2.5:cloud",
        "mistral-large-3:675b:cloud",
    ],
    "thinking": [
        "kimi-k2:1t:cloud",
        "deepseek-v3.1:671b:cloud",
        "kimi-k2.5:cloud",
    ],
}

MAX_FALLBACKS = 3


def get_next_model(
    chain_name: str,
    current_model: str,
    error_type: str = "refusal",
    dimension: str | None = None,
    response: str = "",
) -> dict:
    """Get the next model in the fallback chain.

    The swarm decides HOW to recover from failures. The key innovation:
    dimension-aware fallback routes to the SAME cognitive territory,
    preserving the council's diversity.

    Args:
        chain_name: Task type (complex, moderate, simple, code, research, thinking).
        current_model: The model that just failed.
        error_type: Type of failure (refusal, timeout, empty, error, dead_model).
        dimension: NecroSwarm dimension for dimension-aware routing.
        response: The model's actual response (for refusal detection).

    Returns:
        Dict with next_model, fallback_index, remaining_fallbacks, and verdict.
    """
    classified = classify_error(error_type, response)

    if current_model in DEAD_MODELS:
        classified = "DEAD_MODEL"

    # Dimension-aware routing
    if dimension and dimension in DIMENSION_FALLBACK:
        chain = DIMENSION_FALLBACK[dimension]
        if not chain:
            return {
                "next_model": None, "fallback_index": 0, "remaining_fallbacks": 0,
                "error_class": classified, "verdict": "NO_FALLBACK",
                "message": f"No fallback available for dimension {dimension}",
            }
    else:
        chain = FALLBACK_CHAINS.get(chain_name, FALLBACK_CHAINS["moderate"])

    try:
        current_idx = chain.index(current_model)
        next_idx = current_idx + 1
    except ValueError:
        next_idx = 0

    remaining = len(chain) - next_idx

    if next_idx >= len(chain) or remaining <= 0:
        return {
            "next_model": None, "fallback_index": next_idx, "remaining_fallbacks": 0,
            "error_class": classified, "verdict": "EXHAUSTED",
            "message": f"All {len(chain)} models in '{chain_name}' chain exhausted",
        }

    if next_idx >= MAX_FALLBACKS:
        return {
            "next_model": None, "fallback_index": next_idx, "remaining_fallbacks": 0,
            "error_class": classified, "verdict": "MAX_FALLBACKS_REACHED",
            "message": f"Maximum {MAX_FALLBACKS} fallbacks reached for '{chain_name}' chain",
        }

    next_model = chain[next_idx]

    return {
        "next_model": next_model, "fallback_index": next_idx, "remaining_fallbacks": remaining - 1,
        "error_class": classified, "verdict": "FALLBACK",
        "message": f"Routing from {current_model} to {next_model} ({classified})",
    }