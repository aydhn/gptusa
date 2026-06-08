from typing import Any
from usa_signal_bot.portfolio.foundation.phase153_models import (
    ConstraintValidationReport, PortfolioConstraintCatalog, PortfolioEligibilityRule
)

def build_constraint_validation_report(catalog: PortfolioConstraintCatalog, rules: list[PortfolioEligibilityRule]) -> ConstraintValidationReport:
    report = ConstraintValidationReport()
    report.catalog = catalog
    report.rules = rules

    report.hard_constraint_count = sum(1 for c in catalog.constraints if c.hard_constraint)
    report.soft_constraint_count = sum(1 for c in catalog.constraints if c.soft_constraint)

    for c in catalog.constraints:
        if c.actual_weight_output or c.actual_allocation_output:
            report.actual_weight_output_detected = True
            report.actual_allocation_output_detected = True

    report.report_valid = not report.actual_weight_output_detected and not report.actual_allocation_output_detected and not report.actual_position_size_detected
    return report

def validate_constraint_validation_report(report: ConstraintValidationReport) -> list[str]:
    errors = []
    if report.actual_weight_output_detected:
        errors.append("actual_weight_output_detected must be False")
    if report.actual_allocation_output_detected:
        errors.append("actual_allocation_output_detected must be False")
    if report.actual_position_size_detected:
        errors.append("actual_position_size_detected must be False")
    return errors

def constraint_validation_report_summary(report: ConstraintValidationReport) -> dict[str, Any]:
    return {
        "valid": report.report_valid,
        "hard_constraints": report.hard_constraint_count,
        "soft_constraints": report.soft_constraint_count
    }

def constraint_validation_report_to_text(report: ConstraintValidationReport, limit: int = 300) -> str:
    return f"ConstraintValidationReport: valid={report.report_valid}"
