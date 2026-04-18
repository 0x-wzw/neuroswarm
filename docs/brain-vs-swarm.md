# Brain vs. Swarm: What Goes Where and Why

## The Fundamental Split

NEUROSWARM unifies two systems that solve **different problems**:

| | Brain (WHAT) | Swarm (HOW) |
|---|---|---|
| **Question** | What should we do? | How do we do it well? |
| **Speed** | Sub-millisecond | Seconds to minutes |
| **Method** | Pattern matching, cache lookup | Multi-model deliberation |
| **State** | Persistent (memory, knowledge) | Ephemeral (session deliberation) |
| **LLM Calls** | None (deterministic) | Multiple (council members) |
| **Failure Mode** | No match → fallback | Model refuses → next in chain |

## Phase 1: Brain (WHAT)

The brain is a **deterministic dispatch system**. No LLM calls. It answers:

1. **What skill matches this intent?** → RESOLVER (35+ patterns)
2. **What do we already know?** → Brain-First (memory → sessions)
3. **What signals are in this message?** → Signal Detection (entities, preferences)
4. **Should this entity be enriched?** → Enrichment (tier-based)

### What Goes in the Brain

- ✅ Intent resolution (dispatch table)
- ✅ Memory cache checking
- ✅ Entity extraction and classification
- ✅ Priority classification (HIGH/MEDIUM/LOW)
- ✅ Model suggestion based on complexity
- ❌ LLM calls of any kind
- ❌ Deliberation or consensus
- ❌ Multi-perspective reasoning

### Origin: GBrain

The brain patterns come from Garry Tan's GBrain:
- RESOLVER → GBrain's fat markdown dispatch table, evolved to executable Python
- Signal Detection → GBrain's sub-agent spawn, evolved to local classification
- Brain-First → GBrain's 5-step PGLite lookup, evolved to 2-step memory check
- Enrichment → GBrain's auto-escalation tiers, evolved to signal priority
- Knowledge Store → GBrain's PGLite compound, YAGNI until we need it

## Phase 2: Swarm (HOW)

The swarm is a **deliberative system**. Multiple LLM perspectives. It answers:

1. **Is this worth deliberating?** → Pre-Spawn (3-question gate)
2. **Which models should deliberate?** → Council (dimension assignment)
3. **What if a model refuses?** → Refusal Routing (dimension-aware)
4. **How do we present this to the human?** → Sparring (not approval-seeking)

### What Goes in the Swarm

- ✅ Multi-model deliberation and consensus
- ✅ Spawn decision (complexity? parallel? tokens?)
- ✅ Dimension-aware fallback routing
- ✅ Council verdict synthesis
- ✅ Sparring-mode communication
- ❌ Pattern matching (that's the brain)
- ❌ Intent resolution (that's the brain)
- ❌ Memory caching (that's the brain)

### Origin: NecroSwarm

The swarm patterns are original to NecroSwarm:
- 10-D Council → Original (10 cognitive dimensions, 10 best models)
- Pre-Spawn → Original (3-question gate before spawning)
- Refusal Routing → Evolved from GBrain's flat chain to dimension-aware
- Sparring Mode → Original (humans challenge, agents drive)
- Dimension Map → Original (D1-D10 with configurable models)

## The Bridge

The bridge is where **WHAT** meets **HOW**. Brain context gets packaged
into council deliberation prompts so the swarm doesn't start from zero.

```python
# Without bridge:
# Swarm deliberates from scratch → slower, less informed

# With bridge:
# Swarm sees: memory hits, detected signals, enrichment tiers
# → faster convergence, fewer hallucinations, better context
```

## Why Not Just One System?

**Brain without Swarm** = A library no one reads. You know what to do but
can't deliberate on how to do it well. Single-perspective reasoning.

**Swarm without Brain** = Philosophers arguing in the void. Multiple perspectives
but no shared knowledge base. Every deliberation starts from zero.

**NEUROSWARM** = Both. The brain remembers and directs. The swarm deliberates
and refines. Together, they remember AND reason.