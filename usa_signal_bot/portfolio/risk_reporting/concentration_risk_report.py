from typing import List, Optional
import datetime

from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    PortfolioGovernanceReport,
    SandboxExposureGovernanceRecord,
    create_portfolio_governance_report_id,
    PortfolioRiskMetric,
    create_portfolio_risk_metric_id
)
from usa_signal_bot.core.enums import PortfolioRiskReportKind, PortfolioRiskMetricKind

def build_concentration_risk_report(exposure_records: List[SandboxExposureGovernanceRecord]) -> PortfolioGovernanceReport:
    metrics = []

    max_w = calculate_max_sandbox_weight(exposure_records)
    if max_w is not None:
        metrics.append(PortfolioRiskMetric(
            metric_id=create_portfolio_risk_metric_id(),
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            metric_kind=PortfolioRiskMetricKind.MAX_SANDBOX_WEIGHT,
            name="Max Sandbox Weight",
            value=max_w,
            method_name=None,
            report_kind=PortfolioRiskReportKind.CONCENTRATION_RISK,
            metric_valid=True,
            research_metric_only=True,
            not_investment_advice=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))

    top_5 = calculate_top_n_sandbox_concentration(exposure_records, 5)
    if top_5 is not None:
         metrics.append(PortfolioRiskMetric(
            metric_id=create_portfolio_risk_metric_id(),
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            metric_kind=PortfolioRiskMetricKind.TOP_N_CONCENTRATION,
            name="Top 5 Sandbox Concentration",
            value=top_5,
            method_name=None,
            report_kind=PortfolioRiskReportKind.CONCENTRATION_RISK,
            metric_valid=True,
            research_metric_only=True,
            not_investment_advice=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))

    return PortfolioGovernanceReport(
        report_id=create_portfolio_governance_report_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        report_kind=PortfolioRiskReportKind.CONCENTRATION_RISK,
        title="Concentration Risk Report",
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

def calculate_max_sandbox_weight(exposure_records: List[SandboxExposureGovernanceRecord]) -> Optional[float]:
    weights = [r.normalized_sandbox_optimizer_weight for r in exposure_records if r.normalized_sandbox_optimizer_weight is not None]
    return max(weights) if weights else None

def calculate_top_n_sandbox_concentration(exposure_records: List[SandboxExposureGovernanceRecord], n: int = 5) -> Optional[float]:
    weights = [r.normalized_sandbox_optimizer_weight for r in exposure_records if r.normalized_sandbox_optimizer_weight is not None]
    weights.sort(reverse=True)
    return sum(weights[:n]) if weights else None

def validate_concentration_risk_report(report: PortfolioGovernanceReport) -> List[str]:
    return []
