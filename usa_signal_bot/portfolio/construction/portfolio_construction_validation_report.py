from typing import Any, Dict, List
from usa_signal_bot.portfolio.construction.phase155_models import (
    PortfolioConstructionValidationReport,
    PortfolioConstructionPolicy,
    SandboxAllocationMethodContract,
    AllocationSandboxComparisonReport,
    create_portfolio_construction_validation_report_id,
    _now_str
)
from usa_signal_bot.core.enums import PortfolioConstructionRiskFlag

def build_portfolio_construction_validation_report(
    policy: PortfolioConstructionPolicy,
    contracts: List[SandboxAllocationMethodContract],
    comparison_report: AllocationSandboxComparisonReport
) -> PortfolioConstructionValidationReport:

    report = PortfolioConstructionValidationReport(
        report_id=create_portfolio_construction_validation_report_id(),
        created_at_utc=_now_str(),
        policy=policy,
        method_contracts=contracts,
        comparison_report=comparison_report,
        report_valid=True,
        construction_sandbox_valid=True,
        constraint_compliance_valid=True,
        risk_budget_sandbox_valid=True,
        diversification_diagnostics_valid=True,
        no_actual_target_weights=True,
        no_actual_allocation=True,
        no_capital_deployment=True,
        no_order_output=True,
        no_broker_execution=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    return report

def validate_portfolio_construction_validation_report(report: PortfolioConstructionValidationReport) -> List[str]:
    errors = []

    if not report.no_actual_target_weights:
        errors.append("no_actual_target_weights is False.")
        report.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_TARGET_WEIGHT_RISK)
    if not report.no_actual_allocation:
        errors.append("no_actual_allocation is False.")
        report.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_ALLOCATION_RISK)
    if not report.no_capital_deployment:
        errors.append("no_capital_deployment is False.")
        report.risk_flags.append(PortfolioConstructionRiskFlag.CAPITAL_DEPLOYMENT_RISK)
    if not report.no_order_output:
        errors.append("no_order_output is False.")
        report.risk_flags.append(PortfolioConstructionRiskFlag.ORDER_SIZE_RISK)
    if not report.no_broker_execution:
        errors.append("no_broker_execution is False.")
        report.risk_flags.append(PortfolioConstructionRiskFlag.BROKER_RISK)

    return errors

def portfolio_construction_validation_report_summary(report: PortfolioConstructionValidationReport) -> Dict[str, Any]:
    return {
        "report_id": report.report_id,
        "valid": report.report_valid,
        "no_actual_target_weights": report.no_actual_target_weights,
        "no_actual_allocation": report.no_actual_allocation
    }

def portfolio_construction_validation_report_to_text(report: PortfolioConstructionValidationReport, limit: int = 300) -> str:
    summary = portfolio_construction_validation_report_summary(report)
    return (
        f"Portfolio Construction Validation Report: {summary['report_id']}\n"
        f"Valid: {summary['valid']}\n"
        f"No Actual Target Weights: {summary['no_actual_target_weights']}\n"
        f"No Actual Allocation: {summary['no_actual_allocation']}"
    )
