# GBrain Patterns: Adopted and Rejected

## Source

GBrain (garrytan/gbrain, 8.9k stars) is Garry Tan's opinionated OpenClaw/Hermes
agent brain. It pioneered several patterns that NEUROSWARM has adopted and evolved.

## Adopted Patterns

### 1. RESOLVER — Intent Dispatch

| | GBrain | NEUROSWARM |
|---|---|---|
| **Format** | Fat markdown table | Executable Python script (resolve.py) |
| **Dispatch** | Pattern-match against skills | 35+ patterns with complexity routing |
| **Fallback** | No fallback → search | No match → council deliberation |
| **Routing** | None | TRIVIAL → SIMPLE → MODERATE → COMPLEX, each with model suggestion |

**Evolution**: GBrain's RESOLVER is a markdown document you read. NEUROSWARM's
is an executable script that returns structured data, routes by complexity,
and escalates to council deliberation when no pattern matches.

### 2. Signal Detection — Always-On Entity Extraction

| | GBrain | NEUROSWARM |
|---|---|---|
| **Method** | Sub-agent spawn on every message | Local regex + classification |
| **Storage** | PGLite knowledge compound | Hermes memory (2.2KB key-value) |
| **Scale** | 17,888 pages, months of compound | Session-based, durable preferences only |
| **Cost** | spawns a sub-agent for every message | zero LLM calls, pure pattern matching |

**Evolution**: GBrain spawns a sub-agent to detect every signal. NEUROSWARM
classifies locally (regex + priority), only escalating to LLM when needed.
Different scope: GBrain compounds knowledge over months. We extract signal
for this session and durable preferences only.

### 3. Brain-First — Check Memory Before External Calls

| | GBrain | NEUROSWARM |
|---|---|---|
| **Steps** | 5 (PGLite → file → web search → compound → generate) | 2 (memory → sessions) |
| **Storage** | PGLite (embedded Postgres) | Hermes memory.md + session transcripts |
| **Scope** | Full knowledge graph | Key facts and preferences |

**Evolution**: GBrain checks a full PGLite knowledge base with 5 steps. We
check a 2.2KB key-value memory and session transcripts. Simpler, but same
principle: **don't do expensive work when you already have the answer.**

### 4. Model Routing

| | GBrain | NEUROSWARM |
|---|---|---|
| **Architecture** | Flat (Opus → DeepSeek → Qwen → Groq) | Dimensional (D1→D2→D7, etc.) |
| **Context** | No awareness of what failed | Dimension-aware (cognitive role preserved) |
| **Configuration** | Hardcoded in convention | Configurable dimension map |

**Evolution**: GBrain routes to the next model in a flat list. NEUROSWARM
routes to the next model *in the same dimension*, preserving cognitive
diversity. If D7 General (glm-5.1) refuses, we don't just go to the next
model in some flat list — we go to another General-class model.

### 5. Refusal Routing

| | GBrain | NEUROSWARM |
|---|---|---|
| **Chains** | 1 flat chain | 6 task-type chains + 10 dimension routes |
| **Awareness** | "Try next model" | "Try next model in this dimension" |
| **Dead model handling** | Hope for the best | Explicit dead model list (qwen3.5:cloud) |

**Evolution**: Same as model routing — dimension-aware fallback preserves
the cognitive role of each council seat, rather than blindly going to the
next model in line.

### 6. Thin Harness, Fat Skills

**Adopted directly.** GBrain's philosophy: the bottleneck is never the
model's intelligence, it's whether the model understands your schema.
Skills are fat markdown documents that encode entire workflows. The
harness (runtime) is thin. Intelligence lives in the skills, not the
infrastructure.

NEUROSWARM adds: skills should also have **executable scripts** — not
just markdown, but Python scripts that can be run standalone or integrated
programmatically. Thin harness, fat skills, + executable validation.

## Rejected Patterns

### ❌ Flat Dispatch

GBrain dispatches `query → tool` in a flat table. We have council
deliberation for COMPLEX tasks. A flat table can't deliberate — it can
only look up. NEUROSWARM resolves, then *deliberates*.

### ❌ Convention-over-Config for Models

GBrain hardcodes Opus/DeepSeek/Qwen/Groq. Our dimension map is
configurable and richer. We don't want hardcoded model names — we want
configurable cognitive dimensions.

### ❌ Single Brain Architecture

GBrain is one knowledge store compound over time. We're a swarm of
models that deliberate. Multi-model deliberation > single-source knowledge
for complex decisions.

### ❌ PGLite Dependency

GBrain requires embedded Postgres. We use Hermes memory + session search.
YAGNI — we'll add a knowledge store when we actually need one.

### ❌ Soul Audit

GBrain's 6-phase identity interview (Who am I? What do I believe? etc.)
is not needed for swarm architecture. We don't need identity — we need
execution.

### ❌ Citation-Fixer

GBrain auto-fixes brain page citations. Our knowledge store doesn't
exist yet (YAGNI), so citation fixing is premature.