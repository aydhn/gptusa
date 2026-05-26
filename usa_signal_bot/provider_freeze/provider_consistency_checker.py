from typing import Any, Dict, List
from usa_signal_bot.provider_freeze.phase114_models import (
    MultiProviderReviewItem,
    ProviderFreezeEvidenceItem,
    create_multi_provider_review_item_id,
    _utcnow_str
)
from usa_signal_bot.core.enums import MultiProviderReviewKind, MultiProviderReviewStatus

def _base_item(kind: MultiProviderReviewKind, name: str) -> MultiProviderReviewItem:
    return MultiProviderReviewItem(
        review_item_id=create_multi_provider_review_item_id(),
        created_at_utc=_utcnow_str(),
        review_kind=kind,
        name=name,
        passed=True,
        status=MultiProviderReviewStatus.PASS,
        rationale="Check passed."
    )

def check_provider_registry_consistency(evidence_items: List[ProviderFreezeEvidenceItem]) -> MultiProviderReviewItem:
    item = _base_item(MultiProviderReviewKind.PROVIDER_REGISTRY_CONSISTENCY, "Provider Registry Consistency")
    # Simulate check: in a real implementation we would inspect evidence_items
    # For now, if abstraction evidence is missing, we fail.
    abs_evidence = next((e for e in evidence_items if e.evidence_name == "phase106_provider_abstraction"), None)
    if not abs_evidence or not abs_evidence.available:
        item.passed = False
        item.status = MultiProviderReviewStatus.FAIL
        item.rationale = "phase106_provider_abstraction evidence missing or unavailable."
    return item

def check_adapter_contract_consistency(evidence_items: List[ProviderFreezeEvidenceItem]) -> MultiProviderReviewItem:
    item = _base_item(MultiProviderReviewKind.ADAPTER_CONTRACT_CONSISTENCY, "Adapter Contract Consistency")
    runtime_ev = next((e for e in evidence_items if e.evidence_name == "phase107_provider_runtime"), None)
    if not runtime_ev or not runtime_ev.available:
        item.passed = False
        item.status = MultiProviderReviewStatus.FAIL
        item.rationale = "phase107_provider_runtime evidence missing or unavailable."
    return item

def check_cache_quality_consistency(evidence_items: List[ProviderFreezeEvidenceItem]) -> MultiProviderReviewItem:
    item = _base_item(MultiProviderReviewKind.CACHE_AND_QUALITY_CONSISTENCY, "Cache and Quality Consistency")
    cache_ev = next((e for e in evidence_items if e.evidence_name == "phase108_provider_cache"), None)
    qual_ev = next((e for e in evidence_items if e.evidence_name == "phase109_provider_quality"), None)

    if not cache_ev or not cache_ev.available or not qual_ev or not qual_ev.available:
        item.passed = False
        item.status = MultiProviderReviewStatus.FAIL
        item.rationale = "Cache or Quality evidence missing or unavailable."
    return item

def check_route_fallback_consistency(evidence_items: List[ProviderFreezeEvidenceItem]) -> MultiProviderReviewItem:
    item = _base_item(MultiProviderReviewKind.ROUTE_AND_FALLBACK_CONSISTENCY, "Route and Fallback Consistency")
    orch_ev = next((e for e in evidence_items if e.evidence_name == "phase110_provider_orchestration"), None)
    if not orch_ev or not orch_ev.available:
        item.passed = False
        item.status = MultiProviderReviewStatus.FAIL
        item.rationale = "phase110_provider_orchestration evidence missing or unavailable."
    return item

def provider_consistency_summary(items: List[MultiProviderReviewItem]) -> Dict[str, Any]:
    return {
        "total": len(items),
        "passed": sum(1 for i in items if i.passed),
        "failed": sum(1 for i in items if not i.passed)
    }
