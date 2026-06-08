from typing import Any
from usa_signal_bot.portfolio.sizing.phase154_models import (
    SizingInputReference, SizingCandidate, SizingPolicy, SizingMethodContract,
    SizingPrototypeResult, SizingComparisonMatrix, SizingSensitivityReport,
    RiskBudgetAdherenceReport, SizingPrototypeContext
)
from usa_signal_bot.portfolio.sizing.sizing_input_resolver import detect_forbidden_sizing_columns

def validate_sizing_input_reference_schema(item: SizingInputReference) -> list[str]:
    errors = []
    if item.forbidden_columns_detected:
        errors.append(f"Forbidden columns detected: {item.forbidden_columns_detected}")
    return errors

def validate_sizing_candidate_schema(item: SizingCandidate) -> list[str]:
    errors = []
    if item.actual_position_size is not None:
        errors.append("Actual position size must be None")
    if item.target_weight is not None:
        errors.append("Target weight must be None")
    if item.allocation is not None:
        errors.append("Allocation must be None")
    return errors

def validate_sizing_policy_schema(item: SizingPolicy) -> list[str]:
    errors = []
    if item.actual_position_sizing_allowed:
        errors.append("actual_position_sizing_allowed must be false")
    return errors

def validate_sizing_method_contract_schema(item: SizingMethodContract) -> list[str]:
    errors = []
    if item.produces_actual_position_size:
        errors.append("produces_actual_position_size must be false")
    return errors

def validate_sizing_prototype_result_schema(item: SizingPrototypeResult) -> list[str]:
    errors = []
    if item.actual_position_size is not None:
        errors.append("actual_position_size must be None")
    return errors

def validate_sizing_comparison_matrix_schema(matrix: SizingComparisonMatrix) -> list[str]:
    errors = []
    if not matrix.no_actual_position_size:
        errors.append("no_actual_position_size must be true")
    return errors

def validate_sizing_sensitivity_report_schema(report: SizingSensitivityReport) -> list[str]:
    errors = []
    if report.actual_position_size_detected:
        errors.append("actual_position_size_detected must be false")
    return errors

def validate_risk_budget_adherence_report_schema(report: RiskBudgetAdherenceReport) -> list[str]:
    errors = []
    if report.actual_position_size_detected:
        errors.append("actual_position_size_detected must be false")
    return errors

def validate_sizing_context_schema(context: SizingPrototypeContext) -> list[str]:
    errors = []
    if not context.ready_for_phase155 and context.phase155_readiness_gate_passed:
         errors.append("Conflict in context state regarding Phase 155 readiness")
    return errors

def validate_sizing_column_names(columns: list[str]) -> list[str]:
    return detect_forbidden_sizing_columns(columns)

def validate_no_forbidden_sizing_columns(columns: list[str]) -> list[str]:
    return detect_forbidden_sizing_columns(columns)

def sizing_schema_summary(errors: list[str]) -> dict[str, Any]:
    return {"valid": len(errors) == 0, "error_count": len(errors)}

def sizing_schema_to_text(errors: list[str]) -> str:
    if errors:
        return f"Schema validation failed: {errors[0]}"
    return "Schema valid."
