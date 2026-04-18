"""
NEUROSWARM Brain — Knowledge Store (Architecture Spec)

RRF (Reciprocal Rank Fusion) hybrid search architecture.
Vector similarity + keyword search fused with dedup.

This is an ARCHITECTURE SPEC only — not yet implemented (YAGNI).
Currently we use brain_first (memory + session_search) for retrieval.
When we need a proper knowledge store, this spec describes the target.

Evolved from GBrain's PGLite/Postgres + pgvector implementation into
a lighter architecture that starts with what we have (Hermes memory +
session transcripts) and can grow into a full RRF system.

Current implementation: brain_first.py (2-step: memory → sessions)
Future implementation: This module.
"""


def reciprocal_rank_fusion(
    vector_results: list[dict],
    keyword_results: list[dict],
    k: int = 60,
) -> list[tuple[str, float]]:
    """RRF algorithm: fuse vector and keyword search results.

    GBrain uses this with PGLite + pgvector. We'll use this
    when we have a vector database.

    Args:
        vector_results: Results from vector/semantic search.
        keyword_results: Results from keyword/FTS search.
        k: RRF constant (default 60, standard value).

    Returns:
        Sorted list of (doc_id, rrf_score) tuples, highest first.
    """
    scores: dict[str, float] = {}

    for rank, result in enumerate(vector_results, start=1):
        doc_id = result.get("id", str(rank))
        scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (k + rank)

    for rank, result in enumerate(keyword_results, start=1):
        doc_id = result.get("id", str(rank))
        scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (k + rank)

    return sorted(scores.items(), key=lambda x: -x[1])


# Architecture spec — implementation path
KNOWLEDGE_STORE_PHASES = {
    "phase_1_convention": {
        "status": "IMPLEMENTED",
        "description": "Use memory + session_search before external calls",
        "module": "neuroswarm.brain.brain_first",
    },
    "phase_2_knowledge_store": {
        "status": "FUTURE",
        "description": "PGLite or ChromaDB for embeddings + RRF fusion",
        "depends_on": "vector_database",
    },
    "phase_3_ingestion": {
        "status": "FUTURE",
        "description": "Auto-index session outcomes, web search results",
        "depends_on": "phase_2_knowledge_store",
    },
}