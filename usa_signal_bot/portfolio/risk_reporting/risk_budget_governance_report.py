from typing import Any, Dict, List
import datetime

from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    PortfolioGovernanceReport,
    create_portfolio_governance_report_id,
    PortfolioRiskMetric
)
from usa_signal_bot.core.enums import PortfolioRiskReportKind

def build_risk_budget_governance_report(optimizer_validation_payload: Dict[str, Any], objective_payload: Dict[str, Any]) -> PortfolioGovernanceReport:
    metrics = extract_risk_budget_usage_metrics(optimizer_validation_payload)
    return PortfolioGovernanceReport(
        report_id=create_portfolio_governance_report_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        report_kind=PortfolioRiskReportKind.RISK_BUDGET_GOVERNANCE,
        title="Risk Budget Governance Report",
        metrics=metrics,
        notes=[],
        report_hash=None,
        report_valid=True,
        research_report_only=True,
        no_actual_target_weights=True,
        no_actual_allocation=True,
        no_order_output=True,
        no_broker_execution=True,
        not_investment_advice=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def extract_risk_budget_usage_metrics(payload: Dict[str, Any]) -> List[PortfolioRiskMetric]:
    return []

def validate_risk_budget_governance_report(report: PortfolioGovernanceReport) -> List[str]:
    return []
