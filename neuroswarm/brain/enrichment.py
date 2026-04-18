"""
NEUROSWARM Brain — Enrichment

Tiered entity enrichment inspired by GBrain's auto-escalation system.
GBrain escalates entities from Tier 3 (stub) → Tier 2 (web enrichment) →
Tier 1 (full pipeline) based on mention frequency.

NEUROSWARM maps this to signal priority:
  HIGH = GBrain Tier 1 (save immediately, full context)
  MEDIUM = GBrain Tier 2 (consider saving, web enrichment)
  LOW = GBrain Tier 3 (stub, skip for now)

The brain decides WHAT to enrich. The swarm decides HOW to verify it.
"""

from enum import Enum
from typing import Any


class EnrichmentTier(Enum):
    """GBrain's enrichment tiers mapped to NEUROSWARM's signal priorities."""
    TIER_1_FULL = "full"      # 8+ mentions or meeting — full pipeline
    TIER_2_WEB = "web"        # 3-7 mentions — web + social enrichment
    TIER_3_STUB = "stub"      # 1-2 mentions — stub page only


SIGNAL_TIER_MAPPING = {
    "HIGH": EnrichmentTier.TIER_1_FULL,
    "MEDIUM": EnrichmentTier.TIER_2_WEB,
    "LOW": EnrichmentTier.TIER_3_STUB,
}


def compute_enrichment_tier(
    signal_priority: str,
    mention_count: int = 0,
    has_meeting: bool = False,
) -> dict[str, Any]:
    """Determine the enrichment tier for an entity.

    Combines NEUROSWARM's signal priority with GBrain's mention-count
    escalation logic for a dual-signal enrichment decision.

    Args:
        signal_priority: HIGH, MEDIUM, or LOW from signal detection.
        mention_count: How many times this entity has been mentioned.
        has_meeting: Whether a meeting transcript mentions this entity.

    Returns:
        Dict with tier, action, and verification recommendation.
    """
    # Base tier from signal priority
    base_tier = SIGNAL_TIER_MAPPING.get(signal_priority, EnrichmentTier.TIER_3_STUB)

    # Escalation from mention count (GBrain logic)
    if has_meeting or mention_count >= 8:
        tier = EnrichmentTier.TIER_1_FULL
    elif mention_count >= 3:
        tier = max(base_tier, EnrichmentTier.TIER_2_WEB, key=lambda t: t.value)
        tier = EnrichmentTier.TIER_2_WEB
    else:
        tier = base_tier

    # Actions per tier
    actions = {
        EnrichmentTier.TIER_1_FULL: {
            "action": "full_pipeline",
            "steps": [
                "Create/update entity page",
                "Web + social enrichment",
                "Cross-link with related entities",
                "Add to timeline",
                "Verify with council (D8 Verification)",
            ],
            "council_verification": True,
        },
        EnrichmentTier.TIER_2_WEB: {
            "action": "web_enrichment",
            "steps": [
                "Create/update entity page",
                "Web enrichment (search, social)",
                "Cross-link with related entities",
            ],
            "council_verification": False,
        },
        EnrichmentTier.TIER_3_STUB: {
            "action": "stub_only",
            "steps": [
                "Create stub page with name only",
                "Wait for more mentions before enriching",
            ],
            "council_verification": False,
        },
    }

    tier_info = actions[tier]

    return {
        "entity_signal_priority": signal_priority,
        "mention_count": mention_count,
        "has_meeting": has_meeting,
        "tier": tier.value,
        "action": tier_info["action"],
        "steps": tier_info["steps"],
        "council_verification": tier_info["council_verification"],
    }