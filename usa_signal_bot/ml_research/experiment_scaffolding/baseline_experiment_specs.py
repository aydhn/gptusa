from typing import List, Dict, Any, Optional
from usa_signal_bot.core.enums import BaselineExperimentKind, EvaluationMetricKind, EvaluationHarnessKind
from usa_signal_bot.ml_research.experiment_scaffolding.phase138_models import (
    BaselineExperimentSpec,
    BaselineModelFamilySpec,
    create_baseline_experiment_spec_id,
    _now_utc
)
from usa_signal_bot.ml_research.experiment_scaffolding.baseline_model_family_registry import build_default_baseline_model_family_specs

def build_classification_baseline_experiment(name: str, model_family: BaselineModelFamilySpec, label_name: Optional[str] = None) -> BaselineExperimentSpec:
    return BaselineExperimentSpec(
        experiment_id=create_baseline_experiment_spec_id(),
        created_at_utc=_now_utc(),
        experiment_name=name,
        experiment_kind=BaselineExperimentKind.CLASSIFICATION_BASELINE,
        model_family=model_family,
        dataset_manifest_id=None,
        split_assignment_id=None,
        target_name=None,
        label_name=label_name or "label",
        feature_scope=["*"],
        metric_kinds=[EvaluationMetricKind.CLASSIFICATION_ACCURACY, EvaluationMetricKind.CLASSIFICATION_BALANCED_ACCURACY, EvaluationMetricKind.CLASSIFICATION_F1_MACRO],
        evaluation_harness_kind=EvaluationHarnessKind.OFFLINE_RESEARCH_EVALUATION,
        reproducibility_seed=42,
        training_deferred_to_phase139=True,
        prediction_deferred_to_phase139=True,
        evaluation_deferred_until_artifacts_exist=True,
        research_metadata_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        model_training_used=False,
        model_prediction_used=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False
    )

def build_regression_baseline_experiment(name: str, model_family: BaselineModelFamilySpec, target_name: Optional[str] = None) -> BaselineExperimentSpec:
    return BaselineExperimentSpec(
        experiment_id=create_baseline_experiment_spec_id(),
        created_at_utc=_now_utc(),
        experiment_name=name,
        experiment_kind=BaselineExperimentKind.REGRESSION_BASELINE,
        model_family=model_family,
        dataset_manifest_id=None,
        split_assignment_id=None,
        target_name=target_name or "target",
        label_name=None,
        feature_scope=["*"],
        metric_kinds=[EvaluationMetricKind.REGRESSION_MAE, EvaluationMetricKind.REGRESSION_RMSE, EvaluationMetricKind.REGRESSION_R2],
        evaluation_harness_kind=EvaluationHarnessKind.OFFLINE_RESEARCH_EVALUATION,
        reproducibility_seed=42,
        training_deferred_to_phase139=True,
        prediction_deferred_to_phase139=True,
        evaluation_deferred_until_artifacts_exist=True,
        research_metadata_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        model_training_used=False,
        model_prediction_used=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False
    )

def build_default_baseline_experiment_specs(dataset_manifest_payload: Optional[Dict[str, Any]] = None, split_assignment_payload: Optional[Dict[str, Any]] = None, model_families: Optional[List[BaselineModelFamilySpec]] = None) -> List[BaselineExperimentSpec]:
    if model_families is None:
        model_families = build_default_baseline_model_family_specs()

    cls_families = [f for f in model_families if f.experiment_kind == BaselineExperimentKind.CLASSIFICATION_BASELINE]
    reg_families = [f for f in model_families if f.experiment_kind == BaselineExperimentKind.REGRESSION_BASELINE]
    regime_families = [f for f in model_families if f.experiment_kind == BaselineExperimentKind.REGIME_CONTEXT_BASELINE]

    specs = []
    if cls_families:
        specs.append(build_classification_baseline_experiment("dummy_return_bucket_classification_baseline", cls_families[0]))
        specs.append(build_classification_baseline_experiment("dummy_volatility_bucket_classification_baseline", cls_families[0]))
    if regime_families:
        specs.append(build_classification_baseline_experiment("persistence_regime_context_classification_baseline", regime_families[0]))
    if reg_families:
        specs.append(build_regression_baseline_experiment("dummy_forward_return_regression_baseline", reg_families[0]))
        specs.append(build_regression_baseline_experiment("moving_average_forward_return_regression_baseline", reg_families[-1]))
    if len(cls_families) > 1:
        specs.append(build_classification_baseline_experiment("linear_forward_return_placeholder", cls_families[1]))

    # Inject manifest IDs if available
    for spec in specs:
        if dataset_manifest_payload:
            spec.dataset_manifest_id = dataset_manifest_payload.get("manifest_id")
        if split_assignment_payload:
            spec.split_assignment_id = split_assignment_payload.get("assignment_id")

    return specs

def validate_baseline_experiment_specs(items: List[BaselineExperimentSpec]) -> List[str]:
    errors = []
    if not items:
        errors.append("No experiment specs provided.")
    for item in items:
        if not item.training_deferred_to_phase139:
            errors.append(f"training_deferred_to_phase139 is false for {item.experiment_name}")
        if not item.prediction_deferred_to_phase139:
            errors.append(f"prediction_deferred_to_phase139 is false for {item.experiment_name}")
        if not item.evaluation_deferred_until_artifacts_exist:
            errors.append(f"evaluation_deferred_until_artifacts_exist is false for {item.experiment_name}")
        if item.model_training_used or item.model_prediction_used:
            errors.append(f"Model training/prediction used in {item.experiment_name}")
        if item.produces_trade_signal or item.produces_order_decision or item.produces_portfolio_weights:
            errors.append(f"Trade signal/order semantics enabled in {item.experiment_name}")
        if item.activation_allowed or item.strategy_activation_allowed or item.deployment_allowed:
            errors.append(f"Activation/deployment allowed in {item.experiment_name}")
    return errors

def baseline_experiment_specs_summary(items: List[BaselineExperimentSpec]) -> Dict[str, Any]:
    errors = validate_baseline_experiment_specs(items)
    return {
        "valid": len(errors) == 0,
        "count": len(items),
        "kinds": list(set(i.experiment_kind.value for i in items)),
        "errors": errors
    }

def baseline_experiment_specs_to_text(items: List[BaselineExperimentSpec], limit: int = 300) -> str:
    summary = baseline_experiment_specs_summary(items)
    out = [
        f"Valid: {summary['valid']}",
        f"Count: {summary['count']}",
        f"Kinds: {', '.join(summary['kinds'])}"
    ]
    if summary["errors"]:
        out.append(f"Errors: {', '.join(summary['errors'])}")
    return "\n".join(out)
