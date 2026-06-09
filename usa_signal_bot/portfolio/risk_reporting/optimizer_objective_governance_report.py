from typing import Any, Dict, List
import datetime

from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    PortfolioGovernanceReport,
    create_portfolio_governance_report_id,
    PortfolioRiskMetric
)
from usa_signal_bot.core.enums import PortfolioRiskReportKind

def build_optimizer_objective_governance_report(objective_comparison_payload: Dict[str, Any]) -> PortfolioGovernanceReport:
    metrics = extract_objective_score_metrics(objective_comparison_payload)
    return PortfolioGovernanceReport(
        report_id=create_portfolio_governance_report_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        report_kind=PortfolioRiskReportKind.OBJECTIVE_GOVERNANCE,
        title="Optimizer Objective Governance Report",
        metrics=metrics,
        notes=["best method denotes objective comparison diagnostic only and is not investment advice."],
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

def extract_objective_score_metrics(objective_comparison_payload: Dict[str, Any]) -> List[PortfolioRiskMetric]:
    return []

def validate_optimizer_objective_governance_report(report: PortfolioGovernanceReport) -> List[str]:
    return []
