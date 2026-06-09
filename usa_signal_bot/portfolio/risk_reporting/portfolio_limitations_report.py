from typing import List
import datetime

from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    PortfolioGovernanceReport,
    create_portfolio_governance_report_id
)
from usa_signal_bot.core.enums import PortfolioRiskReportKind

def build_portfolio_limitations_report() -> PortfolioGovernanceReport:
    return PortfolioGovernanceReport(
        report_id=create_portfolio_governance_report_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        report_kind=PortfolioRiskReportKind.LIMITATIONS,
        title="Portfolio Limitations Report",
        metrics=[],
        notes=portfolio_limitations_notes(),
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

def portfolio_limitations_notes() -> List[str]:
    return [
        "Sandbox optimizer output is not an actual target weight.",
        "Risk report is not investment advice.",
        "Live/paper/broker trading is explicitly disabled.",
        "Actual capital allocation is not allowed.",
        "Capital deployment is not allowed.",
        "Backtest/optimizer artifacts are restricted to historical/research-only contexts.",
        "Phase 158 integration handoff is not a deployment approval."
    ]

def validate_portfolio_limitations_report(report: PortfolioGovernanceReport) -> List[str]:
    return []
