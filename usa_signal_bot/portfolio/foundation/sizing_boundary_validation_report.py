from typing import Any
from usa_signal_bot.portfolio.foundation.phase153_models import (
    SizingBoundaryValidationReport, PositionSizingBoundaryContract, PortfolioConstructionBoundary
)

def build_sizing_boundary_validation_report(boundary: PositionSizingBoundaryContract, construction_boundary: PortfolioConstructionBoundary) -> SizingBoundaryValidationReport:
    report = SizingBoundaryValidationReport()
    report.boundary = boundary
    report.construction_boundary = construction_boundary

    report.no_actual_position_size = boundary.no_actual_position_size_phase153
    report.no_target_weight = boundary.no_target_weight_phase153
    report.no_allocation = boundary.no_allocation_phase153
    report.no_capital_deployment = boundary.no_capital_deployment_phase153
    report.no_order_size = boundary.no_order_size_phase153
    report.ready_for_phase154_sizing_prototypes = boundary.sizing_prototype_allowed_phase154

    report.report_valid = (
        report.no_actual_position_size and
        report.no_target_weight and
        report.no_allocation and
        report.no_capital_deployment and
        report.no_order_size
    )

    return report

def validate_sizing_boundary_validation_report(report: SizingBoundaryValidationReport) -> list[str]:
    errors = []
    if not report.no_actual_position_size:
        errors.append("no_actual_position_size must be True")
    if not report.no_target_weight:
        errors.append("no_target_weight must be True")
    if not report.no_allocation:
        errors.append("no_allocation must be True")
    if not report.no_capital_deployment:
        errors.append("no_capital_deployment must be True")
    if not report.no_order_size:
        errors.append("no_order_size must be True")
    if not report.ready_for_phase154_sizing_prototypes:
        errors.append("ready_for_phase154_sizing_prototypes must be True")
    return errors

def sizing_boundary_validation_report_summary(report: SizingBoundaryValidationReport) -> dict[str, Any]:
    return {
        "valid": report.report_valid,
        "ready_for_phase154": report.ready_for_phase154_sizing_prototypes
    }

def sizing_boundary_validation_report_to_text(report: SizingBoundaryValidationReport, limit: int = 300) -> str:
    return f"SizingBoundaryValidationReport: valid={report.report_valid}"
