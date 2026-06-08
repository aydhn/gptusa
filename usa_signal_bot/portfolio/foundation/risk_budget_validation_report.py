from typing import Any
from usa_signal_bot.portfolio.foundation.phase153_models import (
    RiskBudgetValidationReport, RiskBudgetContract
)

def build_risk_budget_validation_report(contract: RiskBudgetContract) -> RiskBudgetValidationReport:
    report = RiskBudgetValidationReport()
    report.contract = contract
    report.budget_item_count = contract.item_count

    for item in contract.items:
        if item.actual_capital_allocation:
            report.actual_capital_allocation_detected = True
        if item.actual_position_size:
            report.actual_position_size_detected = True

    if not contract.no_target_weights:
        report.target_weight_detected = True
    if not contract.no_portfolio_optimization:
        report.portfolio_optimization_detected = True

    report.report_valid = not (report.actual_capital_allocation_detected or report.actual_position_size_detected or report.target_weight_detected or report.portfolio_optimization_detected)
    return report

def validate_risk_budget_validation_report(report: RiskBudgetValidationReport) -> list[str]:
    errors = []
    if report.actual_capital_allocation_detected:
        errors.append("actual_capital_allocation_detected must be False")
    if report.actual_position_size_detected:
        errors.append("actual_position_size_detected must be False")
    if report.target_weight_detected:
        errors.append("target_weight_detected must be False")
    if report.portfolio_optimization_detected:
        errors.append("portfolio_optimization_detected must be False")
    return errors

def risk_budget_validation_report_summary(report: RiskBudgetValidationReport) -> dict[str, Any]:
    return {
        "valid": report.report_valid,
        "budget_items": report.budget_item_count
    }

def risk_budget_validation_report_to_text(report: RiskBudgetValidationReport, limit: int = 300) -> str:
    return f"RiskBudgetValidationReport: valid={report.report_valid}"
