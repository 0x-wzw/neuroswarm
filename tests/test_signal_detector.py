"""Tests for Signal Detection — entity extraction and classification."""

import pytest
from neuroswarm.brain.signal_detector import detect, detect_entities, detect_preferences, classify_signals


class TestDetectEntities:
    """Test entity extraction."""

    def test_url_detection(self):
        result = detect_entities("Check https://github.com/0x-wzw/necroswarm")
        urls = [e for e in result if e["type"] == "url"]
        assert len(urls) >= 1
        assert "github.com" in urls[0]["value"]

    def test_model_name_detection(self):
        result = detect_entities("Use kimi-k2.5 and deepseek-v3.1 for this")
        models = [e for e in result if e["type"] == "model_name"]
        assert len(models) >= 2

    def test_project_name_detection(self):
        result = detect_entities("Update VoidTether and NecroSwarm")
        projects = [e for e in result if e["type"] == "project_name"]
        assert len(projects) >= 2

    def test_tool_name_detection(self):
        result = detect_entities("Run gh and docker commands")
        tools = [e for e in result if e["type"] == "tool_name"]
        assert len(tools) >= 2

    def test_no_entities(self):
        result = detect_entities("the quick brown fox jumps")
        # Should have minimal or no strong entity matches
        assert isinstance(result, list)


class TestDetectPreferences:
    """Test preference extraction."""

    def test_preference_detection(self):
        result = detect_preferences("I prefer autonomous execution")
        assert len(result) >= 1
        assert result[0]["type"] == "preference"

    def test_correction_detection(self):
        result = detect_preferences("Don't ask me for approval, just execute")
        assert len(result) >= 1
        assert result[0]["type"] == "correction"

    def test_directive_detection(self):
        result = detect_preferences("Always add MIT license to repos")
        assert len(result) >= 1
        assert result[0]["type"] == "directive"


class TestClassifySignals:
    """Test signal classification."""

    def test_high_priority_signals(self):
        entities = [{"type": "project_name", "value": "VoidTether", "position": 0}]
        prefs = [{"type": "preference", "text": "I prefer X", "captured": "X", "position": 0}]
        signals = classify_signals(entities, prefs)
        high = [s for s in signals if s["priority"] == "HIGH"]
        assert len(high) >= 1

    def test_low_priority_urls(self):
        entities = [{"type": "url", "value": "https://example.com", "position": 0}]
        signals = classify_signals(entities, [])
        low = [s for s in signals if s["priority"] == "LOW"]
        assert len(low) >= 1


class TestDetect:
    """Test the full detect() function."""

    def test_full_detection(self):
        result = detect("I prefer autonomous execution for VoidTether updates")
        assert "entities" in result
        assert "preferences" in result
        assert "signals" in result
        assert "summary" in result
        assert "memory_actions" in result

    def test_memory_actions(self):
        result = detect("Don't ask me for approval, just execute")
        # Should have save_now recommendations for HIGH signals
        assert len(result["memory_actions"]["save_now"]) >= 1

    def test_dict_output(self):
        result = detect("Use kimi-k2.5 for synthesis")
        assert isinstance(result, dict)