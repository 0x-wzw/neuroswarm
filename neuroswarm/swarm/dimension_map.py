"""
NEUROSWARM Swarm — Dimension Map

The 10-Dimension council configuration. Each dimension maps to a
specific cognitive capability and a specific model in Ollama Cloud.

When a model in a dimension refuses or errors, NEUROSWARM routes
to an adjacent dimension's model, NOT a flat list. This preserves
the cognitive diversity of the council.
"""

# Standard 10-D configuration
DIMENSION_MAP = {
    "D1_synthesis": "kimi-k2.5:cloud",
    "D2_deep_reason": "deepseek-v3.1:671b:cloud",
    "D3_code": "qwen3-coder:480b:cloud",
    "D4_vision": "qwen3-vl:235b:cloud",
    "D5_strategy": "cogito-2.1:671b:cloud",
    "D6_analysis": "mistral-large-3:675b:cloud",
    "D7_general": "glm-5.1:cloud",
    "D8_verification": "nemotron-3-super:cloud",
    "D9_research": "minimax-m2.5:cloud",
    "D10_think": "kimi-k2:1t:cloud",
}

# Dimension-aware fallback: when D_N model fails, route to these
# adjacent dimensions that can cover the same cognitive territory
DIMENSION_FALLBACK = {
    "D1_synthesis": ["deepseek-v3.1:671b:cloud", "glm-5.1:cloud"],
    "D2_deep_reason": ["kimi-k2.5:cloud", "glm-5.1:cloud"],
    "D3_code": ["deepseek-v3.1:671b:cloud", "devstral-2:123b:cloud"],
    "D4_vision": [],  # Vision is specialized, limited fallback
    "D5_strategy": ["kimi-k2.5:cloud", "deepseek-v3.1:671b:cloud"],
    "D6_analysis": ["kimi-k2.5:cloud", "glm-5.1:cloud"],
    "D7_general": ["kimi-k2.5:cloud", "minimax-m2.5:cloud"],
    "D8_verification": ["deepseek-v3.1:671b:cloud", "glm-5.1:cloud"],
    "D9_research": ["kimi-k2.5:cloud", "mistral-large-3:675b:cloud"],
    "D10_think": ["deepseek-v3.1:671b:cloud", "kimi-k2.5:cloud"],
}

# Tier descriptions for documentation
DIMENSION_DESCRIPTIONS = {
    "D1_synthesis": "Converge perspectives into coherent whole",
    "D2_deep_reason": "Analyze deeply, find hidden implications",
    "D3_code": "Generate, review, verify code",
    "D4_vision": "See and interpret visual information",
    "D5_strategy": "Plan strategically, weigh trade-offs",
    "D6_analysis": "Break down complex systems quantitatively",
    "D7_general": "Fast general-purpose reasoning",
    "D8_verification": "Fact-check, accuracy gate",
    "D9_research": "Gather and synthesize information",
    "D10_think": "Slow, thorough, second-order reasoning",
}

# Which dimensions participate in brain phase (WHAT)
BRAIN_PHASE_DIMENSIONS = ["D1_synthesis", "D2_deep_reason", "D5_strategy", "D6_analysis", "D7_general", "D8_verification", "D9_research"]

# Which dimensions participate in swarm phase (HOW) — all of them
SWARM_PHASE_DIMENSIONS = list(DIMENSION_MAP.keys())