"""Tests for Brain-First — memory cache checking."""

import pytest
from neuroswarm.brain.brain_first import brain_check


class TestBrainCheck:
    """Test brain_check() function."""

    def test_returns_dict(self):
        result = brain_check("test query")
        assert isinstance(result, dict)
        assert "query" in result
        assert "memory_check" in result
        assert "session_check" in result
        assert "recommendation" in result

    def test_recommendation_values(self):
        result = brain_check("anything")
        assert result["recommendation"] in ("USE_MEMORY", "CHECK_SESSION", "EXTERNAL_CALL")

    def test_can_skip_external(self):
        result = brain_check("anything")
        assert isinstance(result["can_skip_external"], bool)

    def test_can_skip_when_found(self):
        # If memory finds a match, can_skip_external should be True
        result = brain_check("necroswarm")
        if result["memory_check"]["found"]:
            assert result["can_skip_external"] is True
            assert result["recommendation"] == "USE_MEMORY"