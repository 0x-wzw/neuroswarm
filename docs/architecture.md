# Architecture

## Dual-Phase Dispatch

Every task passes through two phases:

### Phase 1: WHAT (Brain)

The brain determines direction. It answers three questions fast:

1. **What skill matches this intent?** → RESOLVER
2. **What do we already know?** → Brain-First (memory → sessions → web)
3. **What signals are in this message?** → Signal Detection

The brain is **deterministic** — no LLM calls, just pattern matching and cache lookup. Sub-millisecond.

```
Input → RESOLVER → skill, complexity, model
     → Brain-First → memory_hit, cached context
     → Signal Detection → entities, preferences, memory actions
                                ↓
                     brain_context dict
```

### Phase 2: HOW (Swarm)

The swarm determines execution quality. It deliberates among multiple model perspectives.

1. **Is council needed?** → Pre-Spawn Analysis (3-question gate)
2. **Which dimensions deliberate?** → Council configuration
3. **What if a model fails?** → Refusal Routing (dimension-aware)

```
brain_context + task → Pre-Spawn → spawn? or direct?
                                ↓
                    Council Deliberation (if COMPLEX)
                                ↓
                    Verdict + Fallback Chain
                                ↓
                    Context Feed → back to memory
```

### The Bridge: Context Feed

The bridge connects Phase 1 to Phase 2. Brain context gets packaged into
council deliberation prompts so the swarm doesn't start from zero — it
starts from knowledge.

```
brain_context → context_feed.py → deliberation_prompt
                                    ↓
                              Council sees:
                              - Prior knowledge
                              - Detected signals
                              - Memory save recommendations
```

## Module Map

```python
# Phase 1 (Brain)
from neuroswarm.brain.resolver import resolve          # Intent → skill dispatch
from neuroswarm.brain.signal_detector import detect     # Entity extraction
from neuroswarm.brain.brain_first import brain_check   # Memory cache check
from neuroswarm.brain.enrichment import enrich          # Tiered entity enrichment
from neuroswarm.brain.knowledge_store import search      # RRF hybrid (future)

# Phase 2 (Swarm)
from neuroswarm.swarm.council import Council            # Multi-model deliberation
from neuroswarm.swarm.pre_spawn import pre_spawn_check   # 3-question gate
from neuroswarm.swarm.refusal_routing import get_next_model  # Dimension-aware fallback
from neuroswarm.swarm.sparring import format_spar       # Sparring mode messages
from neuroswarm.swarm.dimension_map import DIMENSIONS   # D1-D10 config

# Bridge
from neuroswarm.bridge.context_feed import feed_context   # Brain → Swarm bridge
from neuroswarm.bridge.context_feed import build_deliberation_prompt

# Top-level
from neuroswarm.dispatcher import NeuroSwarmDispatcher  # Full dual-phase dispatch
```

## Data Flow

```
User Query
    │
    ▼
┌─────────────────┐
│   Phase 1: BRAIN │
│   (deterministic) │
│                   │
│  resolve() ──────┤── skill, complexity, model
│  detect() ───────┤── signals, priorities
│  brain_check() ──┤── memory hit/miss
│  enrich() ───────┤── entity tiers
│                   │
│  brain_context ───┤
└────────┬──────────┘
         │
    context_feed()
         │
         ▼
┌─────────────────┐
│  Phase 2: SWARM  │
│  (deliberative)  │
│                  │
│  pre_spawn() ────┤── spawn gate
│  council() ──────┤── verdict
│  fallback() ─────┤── next model
│                  │
│  swarm_result ───┤
└──────────────────┘
         │
    feed_context() ──→ memory (for next time)
         │
         ▼
    ACTION: Execute
```

## Complexity Routing

| Complexity | Brain Only | Swarm | Council Seats |
|---|---|---|---|
| TRIVIAL | ✅ resolve + check | ❌ skip | — |
| SIMPLE | ✅ resolve + check | ❌ skip | — |
| MODERATE | ✅ resolve + check | ✅ quick (2 seats) | D7 + D9 |
| COMPLEX | ✅ resolve + check + signals | ✅ full (3+ seats) | D1 + D2 + D5 |

## Model Fallback Chains

| Task Type | Primary → Fallback 1 → Fallback 2 → Fallback 3 |
|---|---|
| COMPLEX | kimi-k2.5 → deepseek-v3.1 → glm-5.1 → devstral-2 |
| MODERATE | minimax-m2.5 → mistral-large-3 → glm-5.1 |
| SIMPLE | gemma3:27b → glm-5.1 → ministral-3:3b |
| CODE | qwen3-coder:480b → deepseek-v3.1 → devstral-2 |
| RESEARCH | minimax-m2.5 → kimi-k2.5 → mistral-large-3 |
| THINKING | kimi-k2:1t → deepseek-v3.1 → kimi-k2.5 |

Plus 10 dimension-aware routes (D1→D2→D7, etc.) for council seat fallback.