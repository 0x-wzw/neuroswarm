"""
NEUROSWARM Brain — Brain-First Lookup

Check memory and session history BEFORE making external API calls.
Priority: memory → session_search → web_search

Evolved from GBrain's 5-step PGLite lookup into a 2-step check
(memory + session) that's lighter and faster, suited for Hermes'
2.2KB key-value memory rather than a full knowledge store.

The brain checks WHAT we already know before asking the swarm to do more.
"""

import json
import subprocess
from pathlib import Path
from typing import Any

MEMORY_PATH = Path.home() / ".hermes" / "memory.md"


def check_memory(query: str) -> dict[str, Any]:
    """Check Hermes memory file for relevant information.

    Searches the memory markdown file for keyword matches.

    Args:
        query: The information to look for.

    Returns:
        Match info dict with found status and content.
    """
    if not MEMORY_PATH.exists():
        return {"found": False, "source": "memory", "query": query, "content": ""}

    try:
        content = MEMORY_PATH.read_text()
    except Exception:
        return {"found": False, "source": "memory", "query": query, "content": ""}

    entries = content.split("§")
    query_lower = query.lower()
    query_terms = query_lower.split()

    matches = []
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        entry_lower = entry.lower()
        term_hits = sum(1 for term in query_terms if term in entry_lower)
        if term_hits == 0:
            continue
        score = term_hits / len(query_terms) if query_terms else 0
        matches.append({"score": score, "terms_matched": term_hits, "content": entry[:500]})

    if matches:
        matches.sort(key=lambda m: m["score"], reverse=True)
        best = matches[0]
        return {
            "found": best["score"] >= 0.5,
            "source": "memory",
            "query": query,
            "score": best["score"],
            "content": best["content"],
        }

    return {"found": False, "source": "memory", "query": query, "content": ""}


def check_sessions(query: str) -> dict[str, Any]:
    """Check session history for relevant information.

    Searches session transcript files for keyword matches.

    Args:
        query: The information to look for.

    Returns:
        Match info dict.
    """
    sessions_dir = Path.home() / ".hermes" / "sessions"
    if not sessions_dir.exists():
        return {"found": False, "source": "sessions", "query": query, "content": ""}

    query_lower = query.lower()
    query_terms = query_lower.split()
    matches = []

    try:
        for term in query_terms[:3]:
            result = subprocess.run(
                ["grep", "-r", "-l", "-i", term, str(sessions_dir)],
                capture_output=True, text=True, timeout=5,
            )
            if result.returncode == 0:
                for filepath in result.stdout.strip().split("\n"):
                    if filepath:
                        matches.append(filepath)
    except (subprocess.TimeoutExpired, Exception):
        pass

    if matches:
        file_counts = {}
        for f in matches:
            file_counts[f] = file_counts.get(f, 0) + 1
        sorted_files = sorted(file_counts.items(), key=lambda x: -x[1])
        best_file = sorted_files[0][0] if sorted_files else None
        if best_file:
            return {"found": True, "source": "sessions", "query": query, "match_count": len(set(matches)), "best_match": best_file}

    return {"found": False, "source": "sessions", "query": query, "content": ""}


def brain_check(query: str) -> dict[str, Any]:
    """Run the brain-first cache check: memory → sessions → external.

    The brain asks: "Do we already know this?"

    Args:
        query: The information you're looking for.

    Returns:
        Check result with found status, source, and recommendation.
    """
    memory_result = check_memory(query)
    session_result = check_sessions(query) if not memory_result["found"] else {"found": False, "source": "sessions"}

    if memory_result["found"]:
        recommendation = "USE_MEMORY"
        action = "Information found in memory — no external call needed"
        can_skip_external = True
    elif session_result["found"]:
        recommendation = "CHECK_SESSION"
        action = "Information may exist in past sessions — use session_search"
        can_skip_external = True
    else:
        recommendation = "EXTERNAL_CALL"
        action = "No local information found — proceed with web_search or other external call"
        can_skip_external = False

    return {
        "query": query,
        "memory_check": memory_result,
        "session_check": session_result,
        "recommendation": recommendation,
        "can_skip_external": can_skip_external,
        "action": action,
    }