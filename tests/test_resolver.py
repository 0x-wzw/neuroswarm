"""Tests for RESOLVER — intent-to-skill dispatch engine."""

import pytest
from neuroswarm.brain.resolver import resolve, DISPATCH_TABLE, COMPLEXITY_MODEL_ROUTING


class TestResolve:
    """Test the resolve() function."""

    def test_code_intent(self):
        result = resolve("implement the login feature")
        assert result["matches"]
        assert result["primary"]["skill"] == "subagent-driven-development"
        assert result["primary"]["complexity"] == "COMPLEX"

    def test_debug_intent(self):
        result = resolve("debug the authentication error")
        assert result["matches"]
        assert result["primary"]["skill"] == "systematic-debugging"
        assert result["primary"]["complexity"] == "MODERATE"

    def test_research_intent(self):
        result = resolve("research transformer architectures")
        assert result["matches"]
        assert result["primary"]["skill"] == "arxiv"
        assert result["primary"]["complexity"] == "SIMPLE"

    def test_github_intent(self):
        result = resolve("create a new github repo")
        assert result["matches"]
        assert result["primary"]["skill"] == "github-repo-management"

    def test_no_match_triggers_council(self):
        result = resolve("xyzzy foo bar baz quux")
        assert not result["matches"]
        assert "fallback" in result
        assert result["fallback"]["method"] == "necroswarm_council"

    def test_complexity_triggers_council(self):
        result = resolve("spawn council deliberate on plan")
        assert result["matches"]
        assert result["council_deliberation"] is True

    def test_json_output(self):
        result = resolve("deploy model to production")
        assert isinstance(result, dict)
        assert "query" in result
        assert "matches" in result

    def test_specific_over_general(self):
        """More specific patterns should match first."""
        result = resolve("code review the PR")
        # "code review" (17 chars) should beat "code" (4 chars)
        assert result["primary"]["skill"] in ("requesting-code-review", "github-code-review")


class TestModelRouting:
    """Test complexity → model routing."""

    def test_trivial_routing(self):
        assert COMPLEXITY_MODEL_ROUTING["TRIVIAL"] == "ministral-3:3b:cloud"

    def test_simple_routing(self):
        assert COMPLEXITY_MODEL_ROUTING["SIMPLE"] == "gemma3:27b:cloud"

    def test_moderate_routing(self):
        assert COMPLEXITY_MODEL_ROUTING["MODERATE"] == "minimax-m2.5:cloud"

    def test_complex_routing(self):
        assert COMPLEXITY_MODEL_ROUTING["COMPLEX"] == "kimi-k2.5:cloud"


class TestDispatchTable:
    """Test the dispatch table structure."""

    def test_dispatch_table_not_empty(self):
        assert len(DISPATCH_TABLE) > 30  # 35+ patterns documented

    def test_all_entries_have_four_fields(self):
        for entry in DISPATCH_TABLE:
            assert len(entry) == 4  # patterns, skill, category, complexity

    def test_all_complexities_valid(self):
        valid = {"TRIVIAL", "SIMPLE", "MODERATE", "COMPLEX"}
        for entry in DISPATCH_TABLE:
            assert entry[3] in valid