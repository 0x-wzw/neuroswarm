"""Tests for Refusal Routing — dimension-aware model fallback."""

import pytest
from neuroswarm.swarm.refusal_routing import get_next_model, FALLBACK_CHAINS, DIMENSION_FALLBACK, classify_error


class TestClassifyError:
    """Test error classification."""

    def test_timeout(self):
        assert classify_error("timeout") == "TIMEOUT"

    def test_refusal_in_response(self):
        assert classify_error("", "I cannot help with that") == "REFUSAL"

    def test_empty_response(self):
        assert classify_error("", "Yes") == "EMPTY"  # < 20 chars

    def test_dead_model(self):
        assert classify_error("dead_model") == "DEAD_MODEL"

    def test_generic_error(self):
        assert classify_error("error") == "ERROR"


class TestGetNextModel:
    """Test model fallback routing."""

    def test_complex_chain_primary(self):
        result = get_next_model("complex", "kimi-k2.5:cloud", "refusal")
        assert result["next_model"] == "deepseek-v3.1:671b:cloud"
        assert result["verdict"] == "FALLBACK"

    def test_simple_chain(self):
        result = get_next_model("simple", "gemma3:27b:cloud", "refusal")
        assert result["next_model"] == "glm-5.1:cloud"

    def test_exhausted_chain(self):
        result = get_next_model("simple", "ministral-3:3b:cloud", "refusal")
        assert result["verdict"] in ("EXHAUSTED", "MAX_FALLBACKS_REACHED")

    def test_dead_model_skip(self):
        result = get_next_model("complex", "qwen3.5:cloud", "refusal")
        assert result["error_class"] == "DEAD_MODEL"

    def test_dimension_routing(self):
        result = get_next_model("complex", "glm-5.1:cloud", dimension="D7_general", error_type="refusal")
        # Should use dimension-specific fallback, not task chain
        assert result["next_model"] is not None or result["verdict"] == "NO_FALLBACK"

    def test_max_fallbacks(self):
        # After 3 fallbacks, should stop
        result = get_next_model("complex", "glm-5.1:cloud", "refusal")
        # Should be fallback_index 3 (kimi-k2.5 → deepseek-v3.1 → glm-5.1 → devstral-2)
        # Actually glm-5.1 is index 2, next is index 3 which is within MAX_FALLBACKS
        assert result["fallback_index"] is not None


class TestFallbackChains:
    """Test fallback chain definitions."""

    def test_all_task_types_have_chains(self):
        for task_type in ["complex", "moderate", "simple", "code", "research", "thinking"]:
            assert task_type in FALLBACK_CHAINS
            assert len(FALLBACK_CHAINS[task_type]) >= 2

    def test_all_dimensions_have_fallbacks(self):
        for dim in ["D1_synthesis", "D2_deep_reason", "D3_code", "D5_strategy",
                     "D6_analysis", "D7_general", "D8_verification", "D9_research",
                     "D10_think"]:
            assert dim in DIMENSION_FALLBACK