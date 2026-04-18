"""
NEUROSWARM Brain — RESOLVER

Intent-to-skill dispatch engine with complexity routing and council fallback.
Evolved from GBrain's flat markdown dispatch table into an executable Python
module with 35+ intent patterns, complexity-based model routing, and
automatic council escalation for COMPLEX tasks.

The RESOLVER determines WHAT to do. The COUNCIL deliberates HOW.
"""

# ── Dispatch Table ──────────────────────────────────────────────────
# Each entry: (intent_patterns, skill_name, category, complexity)
# Complexity: TRIVIAL, SIMPLE, MODERATE, COMPLEX

DISPATCH_TABLE = [
    # Software Development
    (["code", "implement", "build app", "create feature", "refactor"], "subagent-driven-development", "software-dev", "COMPLEX"),
    (["code review", "review code", "PR review", "review PR"], "requesting-code-review", "software-dev", "MODERATE"),
    (["debug", "error", "failing", "broken", "fix bug", "traceback", "exception"], "systematic-debugging", "software-dev", "MODERATE"),
    (["test", "write test", "TDD", "unit test"], "test-driven-development", "software-dev", "MODERATE"),
    (["plan", "spec", "requirements", "design doc"], "writing-plans", "software-dev", "SIMPLE"),
    (["agent protocol", "A2A", "voidtether", "interoperability"], "agent-interop-bridge", "software-dev", "COMPLEX"),
    (["package", "release", "publish pypi", "semver"], "python-package-release", "software-dev", "MODERATE"),

    # Research
    (["research", "find papers", "arxiv", "paper search"], "arxiv", "research", "SIMPLE"),
    (["monitor blog", "RSS", "feed update"], "blogwatcher", "research", "SIMPLE"),
    (["prediction market", "polymarket", "betting odds"], "polymarket", "research", "SIMPLE"),
    (["write paper", "research paper", "submit paper"], "research-paper-writing", "research", "COMPLEX"),

    # Media
    (["summarize video", "transcript", "youtube"], "youtube-content", "media", "SIMPLE"),
    (["generate video", "render", "html video", "animation"], "hyperframe", "creative", "MODERATE"),
    (["ASCII art", "figlet", "cowsay", "text art"], "ascii-art", "creative", "TRIVIAL"),
    (["diagram", "architecture diagram", "SVG", "system diagram"], "architecture-diagram", "creative", "MODERATE"),
    (["excalidraw", "hand-drawn diagram"], "excalidraw", "creative", "MODERATE"),
    (["manim", "math animation", "3b1b", "explain video"], "manim-video", "creative", "COMPLEX"),
    (["p5.js", "generative art", "creative coding"], "p5js", "creative", "MODERATE"),
    (["song", "music", "lyrics", "suno"], "songwriting-and-ai-music", "creative", "MODERATE"),
    (["GIF", "gif search", "reaction"], "gif-search", "media", "TRIVIAL"),

    # MLOps
    (["serve LLM", "deploy model", "vLLM", "inference server"], "serving-llms-vllm", "mlops", "COMPLEX"),
    (["fine-tune", "LoRA", "train model", "QLoRA"], "axolotl", "mlops", "COMPLEX"),
    (["GGUF", "quantize", "llama.cpp"], "gguf-quantization", "mlops", "MODERATE"),
    (["benchmark", "MMLU", "evaluate LLM"], "evaluating-llms-harness", "mlops", "MODERATE"),
    (["Hugging Face", "hf hub", "upload model"], "huggingface-hub", "mlops", "SIMPLE"),
    (["jailbreak", "red team", "refusal remove"], "godmode", "red-teaming", "MODERATE"),

    # GitHub
    (["github", "create repo", "PR", "issue"], "github-repo-management", "github", "SIMPLE"),
    (["batch repo", "add license to all", "bulk github"], "batch-repo-ops", "github", "SIMPLE"),
    (["converge repo", "merge repo"], "repo-convergence", "github", "COMPLEX"),
    (["codebase inspect", "lines of code", "LOC"], "codebase-inspection", "github", "SIMPLE"),
    (["code review", "review diff"], "github-code-review", "github", "MODERATE"),

    # Productivity
    (["email", "send email", "inbox", "read mail"], "himalaya", "email", "SIMPLE"),
    (["PDF", "edit PDF", "modify PDF"], "nano-pdf", "productivity", "SIMPLE"),
    (["PPT", "powerpoint", "slides", "deck"], "powerpoint", "productivity", "MODERATE"),
    (["obsidian", "notes", "vault"], "obsidian", "note-taking", "SIMPLE"),
    (["notion", "create page", "notion database"], "notion", "productivity", "SIMPLE"),

    # Smart Home / Social / Leisure
    (["smart light", "hue", "philips"], "openhue", "smart-home", "TRIVIAL"),
    (["telegram", "bot config"], "telegram-config", "social", "SIMPLE"),
    (["tweet", "post X", "twitter"], "xitter", "social", "SIMPLE"),
    (["nearby", "restaurant", "find place"], "find-nearby", "leisure", "TRIVIAL"),

    # Orchestration
    (["spawn", "council", "deliberate", "multi-agent"], "necroswarm", "agent-orchestration", "COMPLEX"),
    (["MCP", "tool server", "connect MCP", "mcporter"], "native-mcp", "mcp", "SIMPLE"),

    # Development Tools
    (["claude code", "claude CLI", "delegate coding"], "claude-code", "autonomous-ai-agents", "MODERATE"),
    (["codex", "openai codex"], "codex", "autonomous-ai-agents", "MODERATE"),
    (["opencode", "open code CLI"], "opencode", "autonomous-ai-agents", "MODERATE"),

    # Jupyter / Data
    (["jupyter", "notebook", "data exploration"], "jupyter-live-kernel", "data-science", "SIMPLE"),
]

# Complexity → Model routing (NecroSwarm Ollama Cloud tiers)
COMPLEXITY_MODEL_ROUTING = {
    "TRIVIAL": "ministral-3:3b:cloud",
    "SIMPLE": "gemma3:27b:cloud",
    "MODERATE": "minimax-m2.5:cloud",
    "COMPLEX": "kimi-k2.5:cloud",
}


def resolve(query: str) -> dict:
    """Resolve an intent string to matching skills.

    The brain determines WHAT to do: which skill, how complex, which model,
    and whether the swarm (council) needs to get involved.

    Args:
        query: Natural language intent string.

    Returns:
        Dict with matches, each containing skill, category, complexity,
        suggested model, and council_deliberation flag.
    """
    query_lower = query.lower()
    matches = []

    for patterns, skill, category, complexity in DISPATCH_TABLE:
        for pattern in patterns:
            if pattern in query_lower:
                score = len(pattern)
                matches.append({
                    "skill": skill,
                    "category": category,
                    "complexity": complexity,
                    "matched_pattern": pattern,
                    "suggested_model": COMPLEXITY_MODEL_ROUTING.get(complexity, "glm-5.1:cloud"),
                    "score": score,
                })
                break

    matches.sort(key=lambda x: -x["score"])

    seen_skills = set()
    deduped = []
    for m in matches:
        if m["skill"] not in seen_skills:
            seen_skills.add(m["skill"])
            deduped.append(m)

    if not deduped:
        return {
            "query": query,
            "matches": [],
            "primary": None,
            "council_deliberation": True,  # No match → escalate to council
            "fallback": {
                "method": "necroswarm_council",
                "suggested_model": "kimi-k2.5:cloud",
                "reason": "No dispatch pattern matched — escalate to council deliberation",
            },
        }

    return {
        "query": query,
        "matches": deduped,
        "primary": deduped[0],
        "council_deliberation": any(m["complexity"] == "COMPLEX" for m in deduped),
    }