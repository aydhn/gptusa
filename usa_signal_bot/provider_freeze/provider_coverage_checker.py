from typing import Any, Dict, List
from usa_signal_bot.provider_freeze.phase114_models import (
    MultiProviderReviewItem,
    ProviderFreezeEvidenceItem,
    create_multi_provider_review_item_id,
    _utcnow_str
)
from usa_signal_bot.core.enums import MultiProviderReviewKind, MultiProviderReviewStatus
from usa_signal_bot.provider_freeze.provider_consistency_checker import _base_item

def check_provider_coverage(evidence_items: List[ProviderFreezeEvidenceItem]) -> MultiProviderReviewItem:
    item = _base_item(MultiProviderReviewKind.UNKNOWN, "Overall Provider Coverage")
    gov_ev = next((e for e in evidence_items if e.evidence_name == "phase113_provider_governance"), None)
    if not gov_ev or not gov_ev.available:
        item.passed = False
        item.status = MultiProviderReviewStatus.FAIL
        item.rationale = "Governance evidence missing."
    return item

def check_market_data_coverage(evidence_items: List[ProviderFreezeEvidenceItem]) -> MultiProviderReviewItem:
    item = _base_item(MultiProviderReviewKind.UNKNOWN, "Market Data Coverage")
    # Simulate checking market data coverage. E.g., looking at abstraction evidence
    abs_ev = next((e for e in evidence_items if e.evidence_name == "phase106_provider_abstraction"), None)
    if not abs_ev or not abs_ev.available:
        item.passed = False
        item.status = MultiProviderReviewStatus.FAIL
        item.rationale = "Abstraction evidence missing."
    return item

def check_event_context_coverage(evidence_items: List[ProviderFreezeEvidenceItem]) -> MultiProviderReviewItem:
    item = _base_item(MultiProviderReviewKind.EVENT_CONTEXT_CONSISTENCY, "Event Context Coverage")
    event_ev = next((e for e in evidence_items if e.evidence_name == "phase111_event_metadata"), None)
    impact_ev = next((e for e in evidence_items if e.evidence_name == "phase112_event_impact"), None)
    if not event_ev or not event_ev.available or not impact_ev or not impact_ev.available:
        item.passed = False
        item.status = MultiProviderReviewStatus.FAIL
        item.rationale = "Event metadata or impact evidence missing."
    return item

def provider_coverage_summary(items: List[MultiProviderReviewItem]) -> Dict[str, Any]:
    return {
        "total": len(items),
        "passed": sum(1 for i in items if i.passed),
        "failed": sum(1 for i in items if not i.passed)
    }
