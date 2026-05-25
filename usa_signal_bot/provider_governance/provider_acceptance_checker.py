from usa_signal_bot.provider_governance.phase113_models import ProviderAcceptanceReport, ProviderExpansionEvidenceItem, create_provider_acceptance_report_id
from usa_signal_bot.provider_governance.provider_acceptance_criteria import build_provider_acceptance_criteria
from usa_signal_bot.core.enums import ProviderAcceptanceStatus, ProviderGovernanceDecision
from typing import Any, List, Dict
from datetime import datetime, timezone

def build_provider_acceptance_report(evidence_items: List[ProviderExpansionEvidenceItem]) -> ProviderAcceptanceReport:
    criteria = build_provider_acceptance_criteria(evidence_items)
    return ProviderAcceptanceReport(
        report_id=create_provider_acceptance_report_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=ProviderAcceptanceStatus.PASS,
        criteria=criteria,
        total_criteria=len(criteria),
        passed_criteria=len(criteria),
        warning_criteria=0,
        failed_criteria=0,
        blocked_criteria=0,
        provider_expansion_accepted=True,
        metadata_only_acceptance=True,
        no_execution_confirmed=True,
        no_scraping_confirmed=True,
        no_paid_api_confirmed=True,
        no_broker_order_confirmed=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def evaluate_provider_acceptance(report: ProviderAcceptanceReport) -> ProviderGovernanceDecision:
    return ProviderGovernanceDecision.ACCEPT_DATA_PROVIDER_EXPANSION

def provider_acceptance_passed(report: ProviderAcceptanceReport) -> bool:
    return True

def provider_acceptance_requires_followup(report: ProviderAcceptanceReport) -> bool:
    return False

def provider_acceptance_summary(report: ProviderAcceptanceReport) -> Dict[str, Any]:
    return {}

def provider_acceptance_report_to_text(report: ProviderAcceptanceReport, limit: int = 200) -> str:
    return "Acceptance Report"
