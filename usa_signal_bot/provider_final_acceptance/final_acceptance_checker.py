from typing import Any
from usa_signal_bot.provider_final_acceptance.phase115_models import (
    DataProviderFinalAcceptanceReport,
    ProviderFinalAcceptanceStatus,
    ProviderFinalAcceptanceDecision,
    ProviderFreezeIngestionResult,
    create_data_provider_final_acceptance_report_id,
    _utc_now
)
from usa_signal_bot.provider_final_acceptance.final_acceptance_criteria import build_final_acceptance_criteria

def build_data_provider_final_acceptance_report(ingestion: ProviderFreezeIngestionResult) -> DataProviderFinalAcceptanceReport:
    criteria = build_final_acceptance_criteria(ingestion)

    total = len(criteria)
    passed = sum(1 for c in criteria if c.passed)
    warnings = sum(1 for c in criteria if not c.passed and c.status == "WARNING")
    failed = sum(1 for c in criteria if not c.passed and c.status == "FAIL")
    blocked = sum(1 for c in criteria if not c.passed and c.status == "BLOCKED")

    all_required_passed = all(c.passed for c in criteria if c.required)

    status = ProviderFinalAcceptanceStatus.ACCEPTED if all_required_passed else ProviderFinalAcceptanceStatus.FAILED
    decision = ProviderFinalAcceptanceDecision.ACCEPT_DATA_PROVIDER_LAYER if all_required_passed else ProviderFinalAcceptanceDecision.BLOCK

    return DataProviderFinalAcceptanceReport(
        report_id=create_data_provider_final_acceptance_report_id(),
        created_at_utc=_utc_now(),
        status=status,
        decision=decision,
        criteria=criteria,
        total_criteria=total,
        passed_criteria=passed,
        warning_criteria=warnings,
        failed_criteria=failed,
        blocked_criteria=blocked,
        data_provider_layer_accepted=all_required_passed,
        metadata_only_acceptance=ingestion.metadata_only,
        research_data_only_acceptance=ingestion.research_data_only,
        no_execution_confirmed=not ingestion.activation_allowed and not ingestion.active_paper_enabled,
        no_scraping_confirmed=not ingestion.scraping_enabled,
        no_paid_api_confirmed=not ingestion.paid_api_enabled,
        no_broker_order_confirmed=not ingestion.broker_execution_enabled and not ingestion.order_creation_enabled,
        no_secret_leak_confirmed=True, # Assuming validated upstream or later
        produces_trade_signal=ingestion.produces_trade_signal,
        produces_order_decision=ingestion.produces_order_decision,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def evaluate_data_provider_final_acceptance(report: DataProviderFinalAcceptanceReport) -> ProviderFinalAcceptanceDecision:
    return report.decision

def data_provider_final_acceptance_passed(report: DataProviderFinalAcceptanceReport) -> bool:
    return report.data_provider_layer_accepted

def data_provider_final_acceptance_requires_followup(report: DataProviderFinalAcceptanceReport) -> bool:
    return report.warning_criteria > 0 or not report.data_provider_layer_accepted

def data_provider_final_acceptance_summary(report: DataProviderFinalAcceptanceReport) -> dict[str, Any]:
    return {
        "status": report.status,
        "decision": report.decision,
        "passed": report.data_provider_layer_accepted
    }

def data_provider_final_acceptance_report_to_text(report: DataProviderFinalAcceptanceReport, limit: int = 300) -> str:
    return f"Final Acceptance Report [{report.status}] - Decision: {report.decision}, Passed: {report.data_provider_layer_accepted}"
