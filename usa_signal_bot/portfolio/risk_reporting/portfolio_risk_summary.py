from typing import Any, Dict, List, Optional
import datetime
import hashlib
import json

from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    PortfolioRiskSummary,
    PortfolioRiskMetric,
    SandboxExposureGovernanceRecord,
    PortfolioGovernanceReport,
    create_portfolio_risk_summary_id
)

def build_portfolio_risk_summary(exposure_records: List[SandboxExposureGovernanceRecord], governance_reports: Optional[List[PortfolioGovernanceReport]] = None) -> PortfolioRiskSummary:
    metrics = build_portfolio_risk_metrics(exposure_records)
    if governance_reports:
        for r in governance_reports:
            metrics.extend(r.metrics)

    summary = PortfolioRiskSummary(
        summary_id=create_portfolio_risk_summary_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        metrics=metrics,
        exposure_records=exposure_records,
        method_count=len(set(r.method_name for r in exposure_records)),
        symbol_count=len(set(r.symbol for r in exposure_records)),
        summary_hash=None,
        summary_valid=True,
        research_report_only=True,
        actual_target_weight_detected=False,
        actual_portfolio_weight_detected=False,
        actual_allocation_detected=False,
        actual_position_size_detected=False,
        order_size_detected=False,
        capital_allocation_detected=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    summary.summary_hash = compute_portfolio_risk_summary_hash(summary)
    return summary

def build_portfolio_risk_metrics(exposure_records: List[SandboxExposureGovernanceRecord]) -> List[PortfolioRiskMetric]:
    return []

def compute_portfolio_risk_summary_hash(summary: PortfolioRiskSummary) -> str:
    from usa_signal_bot.portfolio.risk_reporting.phase157_models import portfolio_risk_summary_to_dict
    d = portfolio_risk_summary_to_dict(summary)
    d.pop("summary_hash", None)
    s = json.dumps(d, sort_keys=True)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def validate_portfolio_risk_summary(summary: PortfolioRiskSummary) -> List[str]:
    errs = []
    if summary.actual_target_weight_detected: errs.append("actual_target_weight_detected")
    if summary.actual_portfolio_weight_detected: errs.append("actual_portfolio_weight_detected")
    if summary.actual_allocation_detected: errs.append("actual_allocation_detected")
    if summary.actual_position_size_detected: errs.append("actual_position_size_detected")
    if summary.order_size_detected: errs.append("order_size_detected")
    if summary.capital_allocation_detected: errs.append("capital_allocation_detected")
    if summary.investment_advice: errs.append("investment_advice")
    return errs

def portfolio_risk_summary_to_text(summary: PortfolioRiskSummary, limit: int = 300) -> str:
    return f"Risk Summary: {summary.summary_id}"
