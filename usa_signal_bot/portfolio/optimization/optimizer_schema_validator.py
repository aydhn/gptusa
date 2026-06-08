from typing import Any, Dict, List
import pandas as pd
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerInputReference, OptimizerSandboxCandidate, OptimizerPolicy, OptimizerObjectiveContract, OptimizerConstraintContract, OptimizerSandboxResult, ObjectiveComparisonReport, OptimizerPrototypeContext
from usa_signal_bot.portfolio.optimization.optimizer_input_resolver import detect_forbidden_optimizer_columns

def validate_optimizer_input_reference_schema(item: OptimizerInputReference) -> List[str]:
    return [f"Forbidden cols: {item.forbidden_columns_detected}"] if item.forbidden_columns_detected else []

def validate_optimizer_candidate_schema(item: OptimizerSandboxCandidate) -> List[str]:
    errs = []
    if item.actual_target_weight is not None: errs.append("actual_target_weight not None")
    if item.actual_portfolio_weight is not None: errs.append("actual_portfolio_weight not None")
    return errs

def validate_optimizer_policy_schema(item: OptimizerPolicy) -> List[str]:
    errs = []
    if item.actual_target_weights_allowed: errs.append("actual_target_weights_allowed")
    return errs

def validate_optimizer_objective_contract_schema(item: OptimizerObjectiveContract) -> List[str]:
    errs = []
    if item.produces_actual_target_weight: errs.append("produces_actual_target_weight")
    return errs

def validate_optimizer_constraint_contract_schema(item: OptimizerConstraintContract) -> List[str]:
    errs = []
    if item.produces_actual_target_weight: errs.append("produces_actual_target_weight")
    return errs

def validate_optimizer_result_schema(item: OptimizerSandboxResult) -> List[str]:
    errs = []
    if item.actual_target_weight is not None: errs.append("actual_target_weight not None")
    return errs

def validate_objective_comparison_report_schema(report: ObjectiveComparisonReport) -> List[str]:
    errs = []
    if report.actual_target_weight_detected: errs.append("actual_target_weight_detected")
    return errs

def validate_optimizer_context_schema(context: OptimizerPrototypeContext) -> List[str]:
    errs = []
    if context.actual_target_weights_produced: errs.append("actual_target_weights_produced")
    return errs

def validate_optimizer_column_names(columns: List[str]) -> List[str]:
    return detect_forbidden_optimizer_columns(columns)

def validate_no_forbidden_optimizer_columns(columns: List[str]) -> List[str]:
    return detect_forbidden_optimizer_columns(columns)

def optimizer_schema_summary(errors: List[str]) -> Dict[str, Any]:
    return {"errors": len(errors)}

def optimizer_schema_to_text(errors: List[str]) -> str:
    return str(errors)
