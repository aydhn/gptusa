from typing import Any, Dict, List, Optional
from usa_signal_bot.provider_freeze.phase114_models import (
    MultiProviderReviewItem,
    MultiProviderFinalReviewReport,
    ProviderExpansionFreezeBundle,
    ProviderFreezeEvidenceItem,
    create_multi_provider_review_report_id,
    _utcnow_str
)
from usa_signal_bot.core.enums import MultiProviderReviewStatus

# Imports for specific checkers, to be created next
from usa_signal_bot.provider_freeze.provider_consistency_checker import (
    check_provider_registry_consistency,
    check_adapter_contract_consistency,
    check_cache_quality_consistency,
    check_route_fallback_consistency,
)
from usa_signal_bot.provider_freeze.provider_coverage_checker import (
    check_event_context_coverage,
    check_market_data_coverage,
    check_provider_coverage,
)
from usa_signal_bot.provider_freeze.provider_safety_final_checker import (
    check_no_execution_boundary,
    check_no_scraping_boundary,
    check_no_paid_api_boundary,
    check_no_broker_order_boundary
)

def build_multi_provider_review_items(evidence_items: List[ProviderFreezeEvidenceItem], freeze_bundle: Optional[ProviderExpansionFreezeBundle] = None) -> List[MultiProviderReviewItem]:
    items = []

    items.append(check_provider_registry_consistency(evidence_items))
    items.append(check_adapter_contract_consistency(evidence_items))
    items.append(check_cache_quality_consistency(evidence_items))
    items.append(check_route_fallback_consistency(evidence_items))

    # We map some coverage checks to consistency / coverage reviews
    # Although kind isn't strictly defined for all in the enum, we can use related ones or UNKNOWN with descriptive names
    items.append(check_provider_coverage(evidence_items))
    items.append(check_market_data_coverage(evidence_items))
    items.append(check_event_context_coverage(evidence_items)) # maps to EVENT_CONTEXT_CONSISTENCY internally

    items.append(check_no_execution_boundary(evidence_items))
    items.append(check_no_scraping_boundary(evidence_items))
    items.append(check_no_paid_api_boundary(evidence_items))
    items.append(check_no_broker_order_boundary(evidence_items))

    return items

def build_multi_provider_final_review_report(evidence_items: List[ProviderFreezeEvidenceItem], freeze_bundle: Optional[ProviderExpansionFreezeBundle] = None) -> MultiProviderFinalReviewReport:
    report = MultiProviderFinalReviewReport(
        report_id=create_multi_provider_review_report_id(),
        created_at_utc=_utcnow_str()
    )

    items = build_multi_provider_review_items(evidence_items, freeze_bundle)
    report.items = items
    report.total_items = len(items)

    for item in items:
        if item.status == MultiProviderReviewStatus.PASS:
            report.passed_items += 1
        elif item.status == MultiProviderReviewStatus.WARNING:
            report.warning_items += 1
        elif item.status == MultiProviderReviewStatus.FAIL:
            report.failed_items += 1
        elif item.status == MultiProviderReviewStatus.BLOCKED:
            report.blocked_items += 1

    report.multi_provider_review_passed = (report.failed_items == 0 and report.blocked_items == 0)

    # Simple aggregates based on names/kinds (in a real app we'd map kinds explicitly)
    report.provider_consistency_passed = True # Assumed true unless a related item fails
    report.provider_coverage_passed = True
    report.provider_safety_passed = True
    report.no_execution_boundary_passed = True
    report.no_scraping_boundary_passed = True
    report.no_paid_api_boundary_passed = True
    report.no_broker_order_boundary_passed = True

    for item in items:
        if item.status in [MultiProviderReviewStatus.FAIL, MultiProviderReviewStatus.BLOCKED]:
            if "Consistency" in item.name: report.provider_consistency_passed = False
            if "Coverage" in item.name: report.provider_coverage_passed = False
            if "Boundary" in item.name: report.provider_safety_passed = False
            if "No Execution" in item.name: report.no_execution_boundary_passed = False
            if "No Scraping" in item.name: report.no_scraping_boundary_passed = False
            if "No Paid API" in item.name: report.no_paid_api_boundary_passed = False
            if "No Broker/Order" in item.name: report.no_broker_order_boundary_passed = False

    report.produces_trade_signal = False
    report.produces_order_decision = False

    report.status = MultiProviderReviewStatus.PASS if report.multi_provider_review_passed else MultiProviderReviewStatus.FAIL

    return report

def multi_provider_review_passed(report: MultiProviderFinalReviewReport) -> bool:
    return report.multi_provider_review_passed

def multi_provider_review_summary(report: MultiProviderFinalReviewReport) -> Dict[str, Any]:
    return {
        "status": report.status.value,
        "total_items": report.total_items,
        "passed_items": report.passed_items,
        "warning_items": report.warning_items,
        "failed_items": report.failed_items,
        "blocked_items": report.blocked_items
    }

def multi_provider_review_to_text(report: MultiProviderFinalReviewReport, limit: int = 300) -> str:
    lines = [
        f"Multi-Provider Final Review Report: {report.report_id}",
        f"Status: {report.status.value}",
        f"Items: {report.total_items} (Passed: {report.passed_items}, Warnings: {report.warning_items}, Failed: {report.failed_items}, Blocked: {report.blocked_items})",
    ]
    if not report.multi_provider_review_passed:
        lines.append("Report FAILED or BLOCKED.")

    for i, item in enumerate(report.items[:limit]):
        lines.append(f"  - {item.name}: {item.status.value} - {item.rationale}")

    return "\n".join(lines)
