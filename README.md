# 🧠☠️ NEUROSWARM

> **The Brain decides WHAT. The Swarm deliberates HOW.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)]()

NEUROSWARM is a dual-phase agent architecture that unifies two complementary systems:

- **GBrain** — the knowledge-compounding brain. Signal detection, brain-first lookup, entity enrichment, deterministic-then-LLM fallback. Decides **WHAT** to do.
- **NecroSwarm** — the multi-model deliberation council. 10-dimensional council, dimension-aware fallback, pre-spawn analysis, sparring-mode execution. Deliberates **HOW** to do it well.

Neither system alone is sufficient. GBrain compounds knowledge but can't deliberate between competing strategies. NecroSwarm deliberates powerfully but forgets between sessions. Together, they form a cognitive architecture that remembers AND reasons.

```
  ┌─────────────────────────────────────────────────────────┐
  │                    NEUROSWARM                           │
  │                                                         │
  │   ┌─────────────┐        ┌─────────────────────────┐   │
  │   │   GBrain     │        │      NecroSwarm          │   │
  │   │   (WHAT)     │───────>│      (HOW)               │   │
  │   │              │        │                          │   │
  │   │ • Signal Det │        │ • 10-D Council           │   │
  │   │ • Brain-First│ feed   │ • Pre-Spawn Analysis     │   │
  │   │ • Enrichment │──────->│ • Refusal Routing        │   │
  │   │ • RESOLVER   │ context│ • Dimension-Aware F/O    │   │
  │   │ • RRF Search │        │ • Sparring Mode          │   │
  │   └─────────────┘        └─────────────────────────┘   │
  │          │                          │                    │
  │          │    ┌──────────────┐      │                    │
  │          │    │  NEUROSWARM   │      │                    │
  │          └───>│  Dispatcher   │<─────┘                    │
  │               │  (Dual-Phase) │                           │
  │               └──────┬───────┘                           │
  │                      │                                   │
  │               ┌──────▼───────┐                           │
  │               │   ACTION      │                           │
  │               │   Execute     │                           │
  │               └──────────────┘                            │
  └─────────────────────────────────────────────────────────┘
```

---

## The Two Phases

### Phase 1: WHAT (GBrain)

The brain determines direction. It answers: *What should we do? What do we already know? What matters here?*

| Component | Purpose | Origin |
|-----------|---------|--------|
| **RESOLVER** | Intent → skill dispatch table | GBrain (fat markdown) → NEUROSWARM (executable Python) |
| **Signal Detection** | Always-on entity/idea extraction | GBrain (sub-agent spawn) → NEUROSWARM (local classification) |
| **Brain-First** | Check memory before external calls | GBrain (5-step PGLite lookup) → NEUROSWARM (memory + session check) |
| **Knowledge Store** | Hybrid RRF search (vector + keyword) | GBrain (PGLite/Postgres) → NEUROSWARM (architecture spec, YAGNI) |
| **Enrichment** | Tier-based entity compounding | GBrain (auto-escalation) → NEUROSWARM (signal priority HIGH/MEDIUM/LOW) |

### Phase 2: HOW (NecroSwarm)

The swarm determines execution quality. It answers: *How do we do this well? Which models? What consensus? Fallback to what?*

| Component | Purpose | Origin |
|-----------|---------|--------|
| **Pre-Spawn Analysis** | 3-question gate (complexity? parallel? tokens?) | NecroSwarm original |
| **10-D Council** | Multi-model deliberation by dimension | NecroSwarm original |
| **Refusal Routing** | Dimension-aware model fallback | GBrain (flat chain) → NEUROSWARM (dimension-aware) |
| **Sparring Mode** | Humans challenge, agents drive | NecroSwarm original |
| **F/O Chain** | Primary → fallback → backup per task type | GBrain (flat) → NEUROSWARM (6 task-type chains + 10 dimension routes) |

---

## 🏛️ Ancestry

| Ancestor | Fate | What It Contributed |
|----------|------|---------------------|
| **GBrain** (garrytan/gbrain) | 🧠 BRAIN — absorbed WHAT phase | Knowledge compounding, signal detection, brain-first lookup, enrichment tiers, RESOLVER dispatch, thin-harness-fat-skills philosophy |
| **NecroSwarm** (0x-wzw/necroswarm) | ☠️ SWARM — absorbed HOW phase | 10-D council, dimension-aware fallback, pre-spawn analysis, sparring mode, executable pattern skills, convergent extinction philosophy |
| **GBrain Patterns Adopted** | 🧬 Integrated | RESOLVER, signal detection, brain-first, model routing, refusal routing — evolved from GBrain's markdown conventions into NEUROSWARM's executable scripts |
| **GBrain Patterns NOT Adopted** | ❌ Rejected | Flat dispatch (we have council), convention-over-config (our routing is richer), single-brain (we're a swarm), PGLite dependency (we use Hermes memory) |

---

## 🧠☠️ Philosophical Foundation

### GBrain's Insight: Thin Harness, Fat Skills

> "The bottleneck is never the model's intelligence. The bottleneck is whether the model understands your schema." — Garry Tan

Skills are fat markdown documents that encode entire workflows. The harness (runtime) is thin. Intelligence lives in the skills, not the infrastructure.

### NecroSwarm's Insight: Sovereign Execution

> "13 projects died. One swarm remains. I am the extinction." — NecroSwarm v1.5.2

Agents drive decisions. Humans challenge assumptions. No approval bottlenecks. The swarm deliberates HOW to execute, then converges on the best result.

### NEUROSWARM's Synthesis

The brain and the swarm form a dual-process system:

- **System 1 (Brain)**: Fast, knowledge-retrieving, pattern-matching. "Have we seen this before? What do we already know?"
- **System 2 (Swarm)**: Slow, deliberating, multi-model. "What's the best approach? What do multiple perspectives converge on?"

Neither alone is enough. Knowledge without deliberation is a library no one reads. Deliberation without knowledge is philosophers arguing in the void. **NEUROSWARM is both.**

---

## Architecture

```
neuroswarm/
├── README.md                       # You are here
├── LICENSE                         # MIT
├── neuroswarm/                     # 🧠☠️ Core engine (Python)
│   ├── __init__.py
│   ├── dispatcher.py               # Dual-phase dispatcher (WHAT → HOW)
│   ├── brain/                      # 🧠 WHAT phase (GBrain patterns)
│   │   ├── __init__.py
│   │   ├── resolver.py             # Intent → skill dispatch (35+ patterns)
│   │   ├── signal_detector.py      # Always-on entity extraction
│   │   ├── brain_first.py          # Memory/session cache check
│   │   ├── enrichment.py           # Tiered entity enrichment (Tier 1/2/3)
│   │   └── knowledge_store.py      # RRF hybrid search (architecture spec)
│   ├── swarm/                      # ☠️ HOW phase (NecroSwarm patterns)
│   │   ├── __init__.py
│   │   ├── council.py              # 10-D council deliberation
│   │   ├── pre_spawn.py            # 3-question spawn gate
│   │   ├── refusal_routing.py      # Dimension-aware model fallback
│   │   ├── sparring.py             # Human-agent sparring mode
│   │   └── dimension_map.py        # D1-D10 model configuration
│   └── bridge/                     # 🌉 Brain-Swarm bridge
│       ├── __init__.py
│       └── context_feed.py          # Feed brain context into swarm deliberation
├── skills/                          # 🛠️ Skill files (fat markdown)
│   ├── neuroswarm/                  # ☠️ Core swarm skill
│   │   └── SKILL.md
│   ├── resolver/                    # ⚫ RESOLVER
│   │   ├── SKILL.md
│   │   └── scripts/resolve.py
│   ├── signal-detection/            # 👁️ Always-on extraction
│   │   ├── SKILL.md
│   │   └── scripts/detect.py
│   ├── refusal-routing/             # ⛓️ Model fallback
│   │   ├── SKILL.md
│   │   └── scripts/refusal_route.py
│   ├── brain-first/                 # 🧠 Memory cache check
│   │   ├── SKILL.md
│   │   └── scripts/brain_check.py
│   └── hybrid-search/               # 🔍 RRF architecture spec
│       └── SKILL.md
├── docs/
│   ├── architecture.md              # Full architecture documentation
│   ├── brain-vs-swarm.md            # What goes WHERE and WHY
│   └── gbrain-patterns.md           # GBrain patterns we adopted and rejected
├── tests/
│   ├── test_resolver.py
│   ├── test_signal_detector.py
│   ├── test_refusal_routing.py
│   ├── test_brain_first.py
│   ├── test_council.py
│   └── test_dispatcher.py
└── pyproject.toml                   # Package config
```

---

## Quick Start

### As Skill Files (Hermes Agent)

The skill files in `skills/` are ready to use with Hermes Agent. Copy them to `~/.hermes/skills/agent-orchestration/`:

```bash
cp -r skills/* ~/.hermes/skills/agent-orchestration/
```

Each skill has an executable script in `scripts/` that can be run standalone:

```bash
# Resolve an intent
python skills/resolver/scripts/resolve.py "debug the login error"

# Detect signals in a message
python skills/signal-detection/scripts/detect.py --json "I prefer autonomous execution"

# Get next model in fallback chain
python skills/refusal-routing/scripts/refusal_route.py --task complex --model "kimi-k2.5:cloud" --error refusal

# Check memory before web search
python skills/brain-first/scripts/brain_check.py "voidtether github url"
```

### As Python Package

```bash
pip install -e .
```

```python
from neuroswarm.dispatcher import NeuroSwarmDispatcher

dispatcher = NeuroSwarmDispatcher()

# Phase 1: Brain determines WHAT
what = dispatcher.resolve_intent("debug the login error")
# → skill: systematic-debugging, complexity: MODERATE, model: minimax-m2.5:cloud

# Phase 2: Swarm deliberates HOW
how = dispatcher.deliberate(what)
# → council_seats: [D2, D7, D9], consensus_approach: "...", fallback_chain: [...]

# Full dual-phase dispatch
result = dispatcher.dispatch("debug the login error")
```

---

## Dual-Phase Dispatch

The core innovation of NEUROSWARM is the **dual-phase dispatch**: every task passes through both the brain (WHAT) and the swarm (HOW).

### Phase 1: WHAT (Brain)

```python
from neuroswarm.brain.resolver import resolve

result = resolve("research transformer architectures")
# {
#   "skill": "arxiv",
#   "complexity": "SIMPLE",
#   "model": "gemma3:27b:cloud",
#   "brain_context": {...},  # cached knowledge from memory
#   "council_needed": False  # SIMPLE → no council needed
# }
```

### Phase 2: HOW (Swarm)

```python
from neuroswarm.swarm.council import Council

council = Council()
result = council.deliberate(
    task="Design the API architecture for VoidTether",
    seats=["D1_synthesis", "D2_deep_reason", "D5_strategy"],
    brain_context=result["brain_context"]
)
# {
#   "verdict": "...",
#   "consensus": True,
#   "dissent": [],
#   "fallback_chain": [...]
# }
```

### Combined: NEUROSWARM Dispatcher

```python
from neuroswarm.dispatcher import NeuroSwarmDispatcher

dispatcher = NeuroSwarmDispatcher()
result = dispatcher.dispatch("design the API architecture for VoidTether")
# Phase 1 (WHAT): resolve → skill=agent-interop-bridge, complexity=COMPLEX
# Phase 2 (HOW): council deliberation → D1+D2+D5 converge on approach
# → {skill, complexity, approach, council_verdict, fallback_chain, ...}
```

---

## 10-D Council Configuration

| Dimension | Model | Role | Brain Phase (WHAT) | Swarm Phase (HOW) |
|-----------|-------|------|---------------------|---------------------|
| D1 Synthesis | kimi-k2.5:cloud | Converge perspectives | ✅ Final synthesis | ✅ Council lead |
| D2 Deep Reason | deepseek-v3.1:671b:cloud | Analyze deeply | ✅ Deep analysis | ✅ Challenge assumptions |
| D3 Code | qwen3-coder:480b:cloud | Generate/review code | — | ✅ Code verification |
| D4 Vision | qwen3-vl:235b:cloud | See and interpret | — | ✅ Visual analysis |
| D5 Strategy | cogito-2.1:671b:cloud | Plan strategically | ✅ Strategic options | ✅ Strategy validation |
| D6 Analysis | mistral-large-3:675b:cloud | Break down complexly | ✅ Quantitative | ✅ Risk assessment |
| D7 General | glm-5.1:cloud | Fast general purpose | ✅ Quick classification | ✅ Consensus vote |
| D8 Verification | nemotron-3-super:cloud | Fact-check | ✅ Verify claims | ✅ Accuracy gate |
| D9 Research | minimax-m2.5:cloud | Research synthesis | ✅ Info gathering | ⚠️ Backup (transient) |
| D10 Think | kimi-k2:1t:cloud | Extended reasoning | — | ✅ Slow deliberation |

---

## Dimension-Aware Refusal Routing

When a council model refuses or errors, NEUROSWARM routes to an adjacent dimension rather than a flat list:

```python
from neuroswarm.swarm.refusal_routing import get_next_model

# D7 General (glm-5.1) refused → route to D1 Synthesis (kimi-k2.5)
result = get_next_model(
    chain_name="complex",
    current_model="glm-5.1:cloud",
    dimension="D7_general",
    error_type="refusal"
)
# → next_model: "kimi-k2.5:cloud", verdict: "FALLBACK"
```

This is the key insight GBrain was missing: **a flat fallback chain doesn't know which dimension failed.** NEUROSWARM routes to the dimension's backup, preserving cognitive diversity.

---

## What We Adopted from GBrain

| Pattern | GBrain Version | NEUROSWARM Version | Evolution |
|---------|---------------|-------------------|------------|
| RESOLVER | Flat markdown dispatch table | Executable Python with 35+ patterns, complexity routing, council fallback | Markdown → Script |
| Signal Detection | Sub-agent spawn on every message | Local classification (HIGH/MEDIUM/LOW), no sub-agent needed for simple cases | Always-on → Classified |
| Brain-First | 5-step PGLite lookup | 2-step (memory → sessions), Hermes-native | PGLite → Memory |
| Model Routing | Flat table (Opus → DeepSeek → Qwen → Groq) | Dimension-aware (D1→D2→D7, not flat) | Flat → Dimensional |
| Refusal Routing | Flat fallback (primary → fallback → backup) | 6 task-type chains + 10 dimension routes | Flat → Dimensional |
| Enrichment Tiers | Auto-escalation (Tier 3→2→1) | Signal priority (HIGH/MEDIUM/LOW) | Tier-based → Priority-based |
| Thin Harness, Fat Skills | Convention | **Adopted directly** — executable scripts are thin, skill files are fat | ✅ Adopted |
| Knowledge Compounding | PGLite compound over months | Architecture spec (YAGNI until we need it) | ⏳ Future |

## What We Did NOT Adopt

| Pattern | GBrain Version | Why Not |
|---------|---------------|---------|
| Flat Dispatch | Simple intent→skill table | We have council deliberation for COMPLEX tasks |
| Convention-over-Config for Models | Hardcoded Opus/DeepSeek/Qwen | Our dimension map is configurable and richer |
| Single Brain Architecture | One knowledge store | Multi-model deliberation > single brain |
| PGLite Dependency | Embedded Postgres required | We use Hermes memory + session search (YAGNI) |
| Soul Audit | 6-phase identity interview | Not needed for swarm architecture |
| Citation-Fixer | Auto-fix brain page citations | Our knowledge store doesn't exist yet (YAGNI) |

---

## Comparison

| Feature | GBrain | NecroSwarm | NEUROSWARM |
|---------|--------|------------|------------|
| Decides | WHAT (direction) | HOW (execution) | BOTH |
| Knowledge | PGLite compound | 2.2KB memory | Memory + sessions (future: RRF) |
| Models | Single + sub-agents | 10-dimension council | 10-D council with brain context |
| Fallback | Flat chain | Dimension-aware | Dimension-aware + brain-informed |
| Dispatch | Markdown table | Executable Python | Executable Python + council escalation |
| Signal Detection | Sub-agent spawn | Local classification | Local + escalation |
| Enrichment | Auto-escalation Tiers | Priority (H/M/L) | Priority + council verification |
| Philosophy | Thin harness, fat skills | Sovereign execution | Both: Think THEN execute |
| State | Persistent (git) | Ephemeral (session) | Persistent (memory) + Ephemeral (deliberation) |

---

## Convergence History

| Version | Date | What Died | What Was Born |
|---------|------|-----------|---------------|
| v1.0.0 | Apr 17, 2026 | — | NEUROSWARM born. The brain and the swarm joined. |

### Ancestry Tree

```
GBrain (garrytan/gbrain)              NecroSwarm (0x-wzw/necroswarm)
    │ 17,888 pages                         │ 13 projects consumed
    │ 25 skills                            │ 10 dimensions
    │ PGLite compound                      │ Council deliberation
    │ Thin harness, fat skills              │ Sovereign execution
    │                                      │
    └──────────────┬───────────────────────┘
                   │
                   ▼
            NEUROSWARM v1.0.0
            ═════════════════
            Brain decides WHAT.
            Swarm deliberates HOW.
            Together, they remember AND reason.
```

---

## License

MIT — The brain persists. The swarm endures. The code survives.

---

## Acknowledgments

- **Garry Tan** and the **GBrain** project — for the thin-harness-fat-skills philosophy, signal detection patterns, brain-first convention, model routing, refusal chains, and the conviction that skill files are code.
- **Z Teoh (0x-wzw)** — for NecroSwarm's convergent extinction approach, 10-D council deliberation, dimension-aware fallback, and the sovereign execution philosophy.
- **The 13 projects that died** so NecroSwarm could live. And the 25 skills that made GBrain smart. Their patterns survive in NEUROSWARM's DNA.