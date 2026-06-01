from typing import List, Dict, Any
from usa_signal_bot.ml_research.experiment_scaffolding.phase138_models import (
    BaselineExperimentSpec,
    BaselineModelFamilySpec,
    EvaluationMetricSpec,
    EvaluationHarnessContract,
    PredictionOutputBoundary,
    ModelCardDraft,
    BaselineExperimentRegistry,
    BaselineMLScaffoldingContext
)

def _has_forbidden_semantics(s: str) -> bool:
    s = s.lower()
    forbidden = [
        "buy", "sell", "entry", "exit", "order", "broker", "position",
        "portfolio_weight", "target_weight", "allocation", "paper", "live",
        "demo_order", "live_order", "sent_to_broker", "deploy",
        "production_patch", "strategy_active", "deployment_enabled"
    ]
    # 'signal' is special cased to allow technical things like macd_signal_9, but here we'll just check exact boundaries if needed.
    # We'll stick to the exact list above for now.
    for f in forbidden:
        if f in s:
            return True
    return False

def validate_baseline_experiment_spec_schema(item: BaselineExperimentSpec) -> List[str]:
    errors = []
    if _has_forbidden_semantics(item.experiment_name):
        errors.append(f"Experiment name has forbidden semantics: {item.experiment_name}")
    return errors

def validate_model_family_spec_schema(item: BaselineModelFamilySpec) -> List[str]:
    errors = []
    if _has_forbidden_semantics(item.family_name):
        errors.append(f"Family name has forbidden semantics: {item.family_name}")
    return errors

def validate_evaluation_metric_spec_schema(item: EvaluationMetricSpec) -> List[str]:
    errors = []
    if _has_forbidden_semantics(item.metric_name):
        errors.append(f"Metric name has forbidden semantics: {item.metric_name}")
    return errors

def validate_evaluation_harness_contract_schema(item: EvaluationHarnessContract) -> List[str]:
    errors = []
    return errors

def validate_prediction_output_boundary_schema(item: PredictionOutputBoundary) -> List[str]:
    errors = []
    return errors

def validate_model_card_draft_schema(item: ModelCardDraft) -> List[str]:
    errors = []
    return errors

def validate_experiment_registry_schema(item: BaselineExperimentRegistry) -> List[str]:
    errors = []
    return errors

def validate_baseline_scaffolding_context_schema(context: BaselineMLScaffoldingContext) -> List[str]:
    errors = []
    return errors

def validate_baseline_scaffolding_column_names(columns: List[str]) -> List[str]:
    errors = []
    for c in columns:
        if _has_forbidden_semantics(c):
            # Special case for "signal"
            if "signal" in c.lower() and c.lower() not in ["macd_signal_9"]:
                errors.append(f"Forbidden column name (signal): {c}")
            else:
                errors.append(f"Forbidden column name: {c}")
    return errors

def validate_no_forbidden_baseline_scaffolding_columns(columns: List[str]) -> List[str]:
    return validate_baseline_scaffolding_column_names(columns)

def baseline_scaffolding_schema_summary(errors: List[str]) -> Dict[str, Any]:
    return {"valid": len(errors) == 0, "errors": errors}

def baseline_scaffolding_schema_to_text(errors: List[str]) -> str:
    if not errors:
        return "Schema valid."
    return "Schema errors: " + ", ".join(errors)
