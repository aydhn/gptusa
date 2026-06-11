from typing import List, Dict, Any
from usa_signal_bot.core.enums import BaselineModelFamilyKind, BaselineExperimentKind
from usa_signal_bot.ml_research.experiment_scaffolding.phase138_models import (
    BaselineModelFamilySpec,
    create_baseline_model_family_spec_id,
    PredictionOutputBoundaryKind,
    _now_utc
)

def build_dummy_baseline_family_spec(experiment_kind: BaselineExperimentKind) -> BaselineModelFamilySpec:
    expected_output = PredictionOutputBoundaryKind.RESEARCH_CLASS_LABEL_ONLY if experiment_kind == BaselineExperimentKind.CLASSIFICATION_BASELINE else PredictionOutputBoundaryKind.RESEARCH_REGRESSION_VALUE_ONLY
    return BaselineModelFamilySpec(
        family_id=create_baseline_model_family_spec_id(),
        created_at_utc=_now_utc(),
        family_name=f"Dummy Baseline ({experiment_kind.value})",
        family_kind=BaselineModelFamilyKind.DUMMY,
        experiment_kind=experiment_kind,
        training_allowed_in_phase138=False,
        prediction_allowed_in_phase138=False,
        implementation_deferred_to_phase139=True,
        requires_heavy_dependency=False,
        allowed_dependency_names=["numpy", "pandas"],
        forbidden_dependency_names=["sklearn", "torch", "xgboost", "lightgbm", "catboost"],
        expected_input_matrix_kind="FEATURES",
        expected_target_kind="TARGETS",
        expected_label_kind="LABELS" if experiment_kind == BaselineExperimentKind.CLASSIFICATION_BASELINE else None,
        output_boundary_kind=expected_output,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    )

def build_persistence_baseline_family_spec(experiment_kind: BaselineExperimentKind) -> BaselineModelFamilySpec:
    return BaselineModelFamilySpec(
        family_id=create_baseline_model_family_spec_id(),
        created_at_utc=_now_utc(),
        family_name=f"Persistence Baseline ({experiment_kind.value})",
        family_kind=BaselineModelFamilyKind.PERSISTENCE,
        experiment_kind=experiment_kind,
        training_allowed_in_phase138=False,
        prediction_allowed_in_phase138=False,
        implementation_deferred_to_phase139=True,
        requires_heavy_dependency=False,
        allowed_dependency_names=["pandas"],
        forbidden_dependency_names=["sklearn", "torch", "xgboost", "lightgbm", "catboost"],
        expected_input_matrix_kind="FEATURES",
        expected_target_kind="TARGETS",
        expected_label_kind="LABELS" if experiment_kind == BaselineExperimentKind.CLASSIFICATION_BASELINE else None,
        output_boundary_kind=PredictionOutputBoundaryKind.RESEARCH_SCORE_ONLY,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    )

def build_moving_average_baseline_family_spec(experiment_kind: BaselineExperimentKind) -> BaselineModelFamilySpec:
    return BaselineModelFamilySpec(
        family_id=create_baseline_model_family_spec_id(),
        created_at_utc=_now_utc(),
        family_name=f"Moving Average Baseline ({experiment_kind.value})",
        family_kind=BaselineModelFamilyKind.MOVING_AVERAGE,
        experiment_kind=experiment_kind,
        training_allowed_in_phase138=False,
        prediction_allowed_in_phase138=False,
        implementation_deferred_to_phase139=True,
        requires_heavy_dependency=False,
        allowed_dependency_names=["pandas", "numpy"],
        forbidden_dependency_names=["sklearn", "torch", "xgboost", "lightgbm", "catboost"],
        expected_input_matrix_kind="FEATURES",
        expected_target_kind="TARGETS",
        expected_label_kind="LABELS" if experiment_kind == BaselineExperimentKind.CLASSIFICATION_BASELINE else None,
        output_boundary_kind=PredictionOutputBoundaryKind.RESEARCH_REGRESSION_VALUE_ONLY,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    )

def build_linear_placeholder_family_spec(experiment_kind: BaselineExperimentKind) -> BaselineModelFamilySpec:
    expected_output = PredictionOutputBoundaryKind.RESEARCH_CLASS_LABEL_ONLY if experiment_kind == BaselineExperimentKind.CLASSIFICATION_BASELINE else PredictionOutputBoundaryKind.RESEARCH_REGRESSION_VALUE_ONLY
    return BaselineModelFamilySpec(
        family_id=create_baseline_model_family_spec_id(),
        created_at_utc=_now_utc(),
        family_name=f"Linear Placeholder ({experiment_kind.value})",
        family_kind=BaselineModelFamilyKind.SIMPLE_LINEAR,
        experiment_kind=experiment_kind,
        training_allowed_in_phase138=False,
        prediction_allowed_in_phase138=False,
        implementation_deferred_to_phase139=True,
        requires_heavy_dependency=True,
        allowed_dependency_names=["sklearn"],
        forbidden_dependency_names=["torch", "xgboost", "lightgbm", "catboost"],
        expected_input_matrix_kind="FEATURES",
        expected_target_kind="TARGETS",
        expected_label_kind="LABELS" if experiment_kind == BaselineExperimentKind.CLASSIFICATION_BASELINE else None,
        output_boundary_kind=expected_output,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    )

def build_tree_placeholder_family_spec(experiment_kind: BaselineExperimentKind) -> BaselineModelFamilySpec:
    expected_output = PredictionOutputBoundaryKind.RESEARCH_CLASS_LABEL_ONLY if experiment_kind == BaselineExperimentKind.CLASSIFICATION_BASELINE else PredictionOutputBoundaryKind.RESEARCH_REGRESSION_VALUE_ONLY
    return BaselineModelFamilySpec(
        family_id=create_baseline_model_family_spec_id(),
        created_at_utc=_now_utc(),
        family_name=f"Tree Placeholder ({experiment_kind.value})",
        family_kind=BaselineModelFamilyKind.DUMMY,
        experiment_kind=experiment_kind,
        training_allowed_in_phase138=False,
        prediction_allowed_in_phase138=False,
        implementation_deferred_to_phase139=True,
        requires_heavy_dependency=True,
        allowed_dependency_names=["sklearn", "xgboost", "lightgbm"],
        forbidden_dependency_names=["torch"],
        expected_input_matrix_kind="FEATURES",
        expected_target_kind="TARGETS",
        expected_label_kind="LABELS" if experiment_kind == BaselineExperimentKind.CLASSIFICATION_BASELINE else None,
        output_boundary_kind=expected_output,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    )

def build_default_baseline_model_family_specs() -> List[BaselineModelFamilySpec]:
    return [
        build_dummy_baseline_family_spec(BaselineExperimentKind.CLASSIFICATION_BASELINE),
        build_dummy_baseline_family_spec(BaselineExperimentKind.REGRESSION_BASELINE),
        build_persistence_baseline_family_spec(BaselineExperimentKind.REGIME_CONTEXT_BASELINE),
        build_moving_average_baseline_family_spec(BaselineExperimentKind.REGRESSION_BASELINE),
        build_linear_placeholder_family_spec(BaselineExperimentKind.CLASSIFICATION_BASELINE),
        build_tree_placeholder_family_spec(BaselineExperimentKind.CLASSIFICATION_BASELINE),
    ]

def validate_baseline_model_family_specs(items: List[BaselineModelFamilySpec]) -> List[str]:
    errors = []
    if not items:
        errors.append("No model family specs provided.")
    for item in items:
        if item.training_allowed_in_phase138:
            errors.append(f"training_allowed_in_phase138 is true for {item.family_name}")
        if item.prediction_allowed_in_phase138:
            errors.append(f"prediction_allowed_in_phase138 is true for {item.family_name}")
        if not item.implementation_deferred_to_phase139:
            errors.append(f"implementation_deferred_to_phase139 is false for {item.family_name}")
        if item.produces_trade_signal or item.produces_order_decision or item.produces_portfolio_weights:
            errors.append(f"Trade signal/order semantics enabled for {item.family_name}")
    return errors

def baseline_model_family_registry_summary(items: List[BaselineModelFamilySpec]) -> Dict[str, Any]:
    errors = validate_baseline_model_family_specs(items)
    return {
        "valid": len(errors) == 0,
        "count": len(items),
        "kinds": list(set(i.family_kind.value for i in items)),
        "errors": errors
    }

def baseline_model_family_registry_to_text(items: List[BaselineModelFamilySpec], limit: int = 300) -> str:
    summary = baseline_model_family_registry_summary(items)
    out = [
        f"Valid: {summary['valid']}",
        f"Count: {summary['count']}",
        f"Kinds: {', '.join(summary['kinds'])}"
    ]
    if summary["errors"]:
        out.append(f"Errors: {', '.join(summary['errors'])}")
    return "\n".join(out)
