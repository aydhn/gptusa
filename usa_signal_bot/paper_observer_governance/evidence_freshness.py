from typing import Any
from .observer_governance_models import PromotionEvidenceItem, PromotionEvidenceRefresh, create_promotion_evidence_refresh_id
from usa_signal_bot.core.enums import EvidenceFreshnessStatus
from datetime import datetime, timezone

def calculate_evidence_freshness(items: list[PromotionEvidenceItem], max_age_days: int = 14) -> PromotionEvidenceRefresh:
    for item in items:
        item.status = classify_evidence_item_freshness(item, max_age_days)
        item.fresh = (item.status == EvidenceFreshnessStatus.FRESH)

    available_count = sum(1 for i in items if i.available)
    fresh_count = sum(1 for i in items if i.fresh)
    missing_count = sum(1 for i in items if not i.available)
    stale_count = sum(1 for i in items if i.status == EvidenceFreshnessStatus.STALE)

    status = EvidenceFreshnessStatus.UNKNOWN
    if missing_count > 0: status = EvidenceFreshnessStatus.MISSING
    elif stale_count > 0: status = EvidenceFreshnessStatus.STALE
    elif fresh_count == len(items) and len(items) > 0: status = EvidenceFreshnessStatus.FRESH

    return PromotionEvidenceRefresh(
        refresh_id=create_promotion_evidence_refresh_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        candidate_id=None, evidence_items=items,
        required_count=len(items), available_count=available_count, fresh_count=fresh_count,
        missing_count=missing_count, stale_count=stale_count,
        evidence_score=evidence_freshness_score(items),
        status=status, required_followups=evidence_freshness_followups(items), warnings=[], errors=[]
    )

def classify_evidence_item_freshness(item: PromotionEvidenceItem, max_age_days: int = 14) -> EvidenceFreshnessStatus:
    if not item.available: return EvidenceFreshnessStatus.MISSING
    # Basic mock of date checking
    return EvidenceFreshnessStatus.FRESH

def evidence_freshness_score(items: list[PromotionEvidenceItem]) -> float | None:
    if not items: return None
    fresh = sum(1 for i in items if i.fresh)
    return (fresh / len(items)) * 100.0

def evidence_freshness_followups(items: list[PromotionEvidenceItem]) -> list[str]:
    followups = []
    missing = [i.evidence_type for i in items if not i.available]
    if missing: followups.append(f"Collect missing evidence: {', '.join(missing)}")
    stale = [i.evidence_type for i in items if i.status == EvidenceFreshnessStatus.STALE]
    if stale: followups.append(f"Refresh stale evidence: {', '.join(stale)}")
    return followups

def evidence_freshness_to_text(refresh: PromotionEvidenceRefresh) -> str:
    return f"Score: {refresh.evidence_score}, Status: {refresh.status.value}"
