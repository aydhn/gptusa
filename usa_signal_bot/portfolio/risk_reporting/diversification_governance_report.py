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

def build_diversification_governance_report(exposure_records: List[SandboxExposureGovernanceRecord]) -> PortfolioGovernanceReport:
    metrics = []

    enc = calculate_effective_name_count_from_exposures(exposure_records)
    if enc is not None:
        metrics.append(PortfolioRiskMetric(
            metric_id=create_portfolio_risk_metric_id(),
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            metric_kind=PortfolioRiskMetricKind.EFFECTIVE_NAME_COUNT,
            name="Effective Name Count",
            value=enc,
            method_name=None,
            report_kind=PortfolioRiskReportKind.DIVERSIFICATION_GOVERNANCE,
            metric_valid=True,
            research_metric_only=True,
            not_investment_advice=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))

    herf = calculate_herfindahl_from_exposures(exposure_records)
    if herf is not None:
         metrics.append(PortfolioRiskMetric(
            metric_id=create_portfolio_risk_metric_id(),
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            metric_kind=PortfolioRiskMetricKind.HERFINDAHL_INDEX,
            name="Herfindahl Index",
            value=herf,
            method_name=None,
            report_kind=PortfolioRiskReportKind.DIVERSIFICATION_GOVERNANCE,
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
        report_kind=PortfolioRiskReportKind.DIVERSIFICATION_GOVERNANCE,
        title="Diversification Governance Report",
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

def calculate_effective_name_count_from_exposures(exposure_records: List[SandboxExposureGovernanceRecord]) -> Optional[float]:
    weights = [r.normalized_sandbox_optimizer_weight for r in exposure_records if r.normalized_sandbox_optimizer_weight is not None]
    if not weights: return None
    sum_sq = sum(w*w for w in weights)
    if sum_sq == 0: return 0.0
    return 1.0 / sum_sq

def calculate_herfindahl_from_exposures(exposure_records: List[SandboxExposureGovernanceRecord]) -> Optional[float]:
    weights = [r.normalized_sandbox_optimizer_weight for r in exposure_records if r.normalized_sandbox_optimizer_weight is not None]
    if not weights: return None
    return sum(w*w for w in weights)

def validate_diversification_governance_report(report: PortfolioGovernanceReport) -> List[str]:
    return []
