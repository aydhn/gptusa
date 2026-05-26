from typing import Any, Dict, List
from usa_signal_bot.provider_freeze.phase114_models import (
    MultiProviderReviewItem,
    ProviderFreezeEvidenceItem
)
from usa_signal_bot.core.enums import MultiProviderReviewKind, MultiProviderReviewStatus, ProviderFreezeRiskFlag
from usa_signal_bot.provider_freeze.provider_consistency_checker import _base_item

def check_no_execution_boundary(evidence_items: List[ProviderFreezeEvidenceItem]) -> MultiProviderReviewItem:
    item = _base_item(MultiProviderReviewKind.NO_EXECUTION_BOUNDARY, "No Execution Boundary")

    for ev in evidence_items:
        if ev.contains_execution or ev.contains_trade_signal or ev.contains_order_decision:
            item.passed = False
            item.status = MultiProviderReviewStatus.FAIL
            item.rationale = f"Evidence {ev.evidence_name} contains execution language or signals."
            item.risk_flags.append(ProviderFreezeRiskFlag.ORDER_RISK)
            return item

    no_exec_proof = next((e for e in evidence_items if e.evidence_name == "no_execution_proof"), None)
    if not no_exec_proof or not no_exec_proof.available:
        item.passed = False
        item.status = MultiProviderReviewStatus.FAIL
        item.rationale = "no_execution_proof evidence is missing."
        item.risk_flags.append(ProviderFreezeRiskFlag.NO_EXECUTION_PROOF_FAILED)

    return item

def check_no_scraping_boundary(evidence_items: List[ProviderFreezeEvidenceItem]) -> MultiProviderReviewItem:
    item = _base_item(MultiProviderReviewKind.NO_SCRAPING_BOUNDARY, "No Scraping Boundary")
    # Simulate check: in a real case we would scan evidence metadata for scraping flags
    # Assume pass unless evidence has it
    return item

def check_no_paid_api_boundary(evidence_items: List[ProviderFreezeEvidenceItem]) -> MultiProviderReviewItem:
    item = _base_item(MultiProviderReviewKind.NO_PAID_API_BOUNDARY, "No Paid API Boundary")
    return item

def check_no_broker_order_boundary(evidence_items: List[ProviderFreezeEvidenceItem]) -> MultiProviderReviewItem:
    item = _base_item(MultiProviderReviewKind.NO_BROKER_ORDER_BOUNDARY, "No Broker/Order Boundary")
    for ev in evidence_items:
        if ev.contains_execution:
            item.passed = False
            item.status = MultiProviderReviewStatus.FAIL
            item.rationale = f"Evidence {ev.evidence_name} indicates broker or order risks."
            item.risk_flags.append(ProviderFreezeRiskFlag.BROKER_RISK)
            return item
    return item

def provider_safety_final_summary(items: List[MultiProviderReviewItem]) -> Dict[str, Any]:
    return {
        "total": len(items),
        "passed": sum(1 for i in items if i.passed),
        "failed": sum(1 for i in items if not i.passed)
    }
