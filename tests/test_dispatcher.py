"""Tests for the dual-phase dispatcher."""

import pytest
from neuroswarm.dispatcher import NeuroSwarmDispatcher


class TestDispatcher:
    """Test the full dual-phase dispatch."""

    def test_init(self):
        dispatcher = NeuroSwarmDispatcher()
        assert dispatcher.council is not None

    def test_resolve_intent(self):
        dispatcher = NeuroSwarmDispatcher()
        result = dispatcher.resolve_intent("research transformers")
        assert "primary" in result or "fallback" in result
        assert "brain_context" in result

    def test_simple_task_skips_council(self):
        dispatcher = NeuroSwarmDispatcher()
        brain_result = {
            "primary": {"skill": "arxiv", "complexity": "SIMPLE", "suggested_model": "gemma3:27b:cloud"},
            "query": "research transformers",
            "brain_context": {"memory_hit": False, "memory_source": "EXTERNAL_CALL"},
            "council_needed": False,
        }
        result = dispatcher.deliberate(brain_result)
        assert result["approach"] == "direct_execution"
        assert result["council_verdict"] is None

    def test_complex_task_uses_council(self):
        dispatcher = NeuroSwarmDispatcher()
        brain_result = {
            "primary": {"skill": "subagent-driven-development", "complexity": "COMPLEX"},
            "query": "build the entire API",
            "brain_context": {"memory_hit": False},
            "council_deliberation": True,
        }
        result = dispatcher.deliberate(brain_result)
        assert result["approach"] == "full_council"
        assert result["council_seats"] is not None

    def test_full_dispatch(self):
        dispatcher = NeuroSwarmDispatcher()
        result = dispatcher.dispatch("debug the login error")
        assert "phase_1_what" in result
        assert "phase_2_how" in result
        assert result["phase_1_what"]["query"] == "debug the login error"