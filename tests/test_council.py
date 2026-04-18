"""Tests for Council — multi-model deliberation."""

import pytest
from neuroswarm.swarm.council import Council


class TestCouncil:
    """Test Council deliberation."""

    def test_init_default_seats(self):
        council = Council()
        assert council.seats is not None

    def test_init_custom_seats(self):
        custom = {"D1_synthesis": "kimi-k2.5:cloud", "D7_general": "glm-5.1:cloud"}
        council = Council(seats=custom)
        assert council.seats == custom

    def test_deliberate_simple_task(self):
        council = Council()
        # Simple tasks should not need full council
        result = council.deliberate(
            task="Simple lookup task",
            seats=["D7_general"],
            brain_context={"memory_hit": False},
        )
        assert isinstance(result, dict)

    def test_deliberate_with_context(self):
        council = Council()
        result = council.deliberate(
            task="Design complex system",
            seats=["D1_synthesis", "D2_deep_reason", "D5_strategy"],
            brain_context={"memory_hit": True, "signals": {"total_signals": 3}},
        )
        assert isinstance(result, dict)
        assert "task" in result