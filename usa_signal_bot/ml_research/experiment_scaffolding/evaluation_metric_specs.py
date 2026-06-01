from typing import List, Dict, Any, Optional
from usa_signal_bot.core.enums import EvaluationMetricKind, BaselineExperimentKind
from usa_signal_bot.ml_research.experiment_scaffolding.phase138_models import (
    EvaluationMetricSpec,
    create_evaluation_metric_spec_id,
    _now_utc
)

def build_default_evaluation_metric_specs() -> List[EvaluationMetricSpec]:
    specs = []

    # Classification Accuracy
    specs.append(EvaluationMetricSpec(
        metric_id=create_evaluation_metric_spec_id(),
        created_at_utc=_now_utc(),
        metric_name="classification_accuracy",
        metric_kind=EvaluationMetricKind.CLASSIFICATION_ACCURACY,
        applies_to_experiment_kinds=[BaselineExperimentKind.CLASSIFICATION_BASELINE, BaselineExperimentKind.REGIME_CONTEXT_BASELINE],
        higher_is_better=True,
        requires_probabilities=False,
        requires_class_labels=True,
        requires_regression_values=False,
        aggregation_method="MEAN",
        threshold_free=False,
        non_trading_metric=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    ))

    # Balanced Accuracy
    specs.append(EvaluationMetricSpec(
        metric_id=create_evaluation_metric_spec_id(),
        created_at_utc=_now_utc(),
        metric_name="classification_balanced_accuracy",
        metric_kind=EvaluationMetricKind.CLASSIFICATION_BALANCED_ACCURACY,
        applies_to_experiment_kinds=[BaselineExperimentKind.CLASSIFICATION_BASELINE, BaselineExperimentKind.REGIME_CONTEXT_BASELINE],
        higher_is_better=True,
        requires_probabilities=False,
        requires_class_labels=True,
        requires_regression_values=False,
        aggregation_method="MEAN",
        threshold_free=False,
        non_trading_metric=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    ))

    # F1 Macro
    specs.append(EvaluationMetricSpec(
        metric_id=create_evaluation_metric_spec_id(),
        created_at_utc=_now_utc(),
        metric_name="classification_f1_macro",
        metric_kind=EvaluationMetricKind.CLASSIFICATION_F1_MACRO,
        applies_to_experiment_kinds=[BaselineExperimentKind.CLASSIFICATION_BASELINE, BaselineExperimentKind.REGIME_CONTEXT_BASELINE],
        higher_is_better=True,
        requires_probabilities=False,
        requires_class_labels=True,
        requires_regression_values=False,
        aggregation_method="MEAN",
        threshold_free=False,
        non_trading_metric=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    ))

    # Regression MAE
    specs.append(EvaluationMetricSpec(
        metric_id=create_evaluation_metric_spec_id(),
        created_at_utc=_now_utc(),
        metric_name="regression_mae",
        metric_kind=EvaluationMetricKind.REGRESSION_MAE,
        applies_to_experiment_kinds=[BaselineExperimentKind.REGRESSION_BASELINE, BaselineExperimentKind.VOLATILITY_BASELINE],
        higher_is_better=False,
        requires_probabilities=False,
        requires_class_labels=False,
        requires_regression_values=True,
        aggregation_method="MEAN",
        threshold_free=True,
        non_trading_metric=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    ))

    # Regression RMSE
    specs.append(EvaluationMetricSpec(
        metric_id=create_evaluation_metric_spec_id(),
        created_at_utc=_now_utc(),
        metric_name="regression_rmse",
        metric_kind=EvaluationMetricKind.REGRESSION_RMSE,
        applies_to_experiment_kinds=[BaselineExperimentKind.REGRESSION_BASELINE, BaselineExperimentKind.VOLATILITY_BASELINE],
        higher_is_better=False,
        requires_probabilities=False,
        requires_class_labels=False,
        requires_regression_values=True,
        aggregation_method="MEAN",
        threshold_free=True,
        non_trading_metric=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    ))

    # Regression R2
    specs.append(EvaluationMetricSpec(
        metric_id=create_evaluation_metric_spec_id(),
        created_at_utc=_now_utc(),
        metric_name="regression_r2",
        metric_kind=EvaluationMetricKind.REGRESSION_R2,
        applies_to_experiment_kinds=[BaselineExperimentKind.REGRESSION_BASELINE, BaselineExperimentKind.VOLATILITY_BASELINE],
        higher_is_better=True,
        requires_probabilities=False,
        requires_class_labels=False,
        requires_regression_values=True,
        aggregation_method="MEAN",
        threshold_free=True,
        non_trading_metric=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    ))

    # Rank Correlation
    specs.append(EvaluationMetricSpec(
        metric_id=create_evaluation_metric_spec_id(),
        created_at_utc=_now_utc(),
        metric_name="rank_correlation",
        metric_kind=EvaluationMetricKind.RANK_CORRELATION,
        applies_to_experiment_kinds=[BaselineExperimentKind.REGRESSION_BASELINE, BaselineExperimentKind.CLASSIFICATION_BASELINE],
        higher_is_better=True,
        requires_probabilities=True,
        requires_class_labels=False,
        requires_regression_values=True,
        aggregation_method="MEAN",
        threshold_free=True,
        non_trading_metric=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    ))

    # Calibration Brier Score
    specs.append(EvaluationMetricSpec(
        metric_id=create_evaluation_metric_spec_id(),
        created_at_utc=_now_utc(),
        metric_name="calibration_brier_score",
        metric_kind=EvaluationMetricKind.CALIBRATION_BRIER_SCORE,
        applies_to_experiment_kinds=[BaselineExperimentKind.CLASSIFICATION_BASELINE, BaselineExperimentKind.REGIME_CONTEXT_BASELINE],
        higher_is_better=False,
        requires_probabilities=True,
        requires_class_labels=False,
        requires_regression_values=False,
        aggregation_method="MEAN",
        threshold_free=True,
        non_trading_metric=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    ))

    # Confusion Matrix
    specs.append(EvaluationMetricSpec(
        metric_id=create_evaluation_metric_spec_id(),
        created_at_utc=_now_utc(),
        metric_name="confusion_matrix",
        metric_kind=EvaluationMetricKind.CONFUSION_MATRIX,
        applies_to_experiment_kinds=[BaselineExperimentKind.CLASSIFICATION_BASELINE, BaselineExperimentKind.REGIME_CONTEXT_BASELINE],
        higher_is_better=None,
        requires_probabilities=False,
        requires_class_labels=True,
        requires_regression_values=False,
        aggregation_method="NONE",
        threshold_free=False,
        non_trading_metric=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    ))

    # Stability Metric
    specs.append(EvaluationMetricSpec(
        metric_id=create_evaluation_metric_spec_id(),
        created_at_utc=_now_utc(),
        metric_name="stability_metric",
        metric_kind=EvaluationMetricKind.STABILITY_METRIC,
        applies_to_experiment_kinds=[BaselineExperimentKind.CLASSIFICATION_BASELINE, BaselineExperimentKind.REGRESSION_BASELINE],
        higher_is_better=True,
        requires_probabilities=True,
        requires_class_labels=True,
        requires_regression_values=True,
        aggregation_method="MEAN",
        threshold_free=True,
        non_trading_metric=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    ))

    return specs

def metric_spec_by_kind(kind: EvaluationMetricKind, specs: Optional[List[EvaluationMetricSpec]] = None) -> Optional[EvaluationMetricSpec]:
    specs = specs or build_default_evaluation_metric_specs()
    for s in specs:
        if s.metric_kind == kind:
            return s
    return None

def validate_evaluation_metric_specs(items: List[EvaluationMetricSpec]) -> List[str]:
    errors = []
    if not items:
        errors.append("No metric specs provided.")
    for item in items:
        if not item.non_trading_metric:
            errors.append(f"Metric {item.metric_name} is marked as trading metric")
        if item.produces_trade_signal or item.produces_order_decision or item.produces_portfolio_weights:
            errors.append(f"Metric {item.metric_name} produces trading signals or orders")
    return errors

def evaluation_metric_specs_summary(items: List[EvaluationMetricSpec]) -> Dict[str, Any]:
    errors = validate_evaluation_metric_specs(items)
    return {
        "valid": len(errors) == 0,
        "count": len(items),
        "kinds": list(set(i.metric_kind.value for i in items)),
        "errors": errors
    }

def evaluation_metric_specs_to_text(items: List[EvaluationMetricSpec], limit: int = 300) -> str:
    summary = evaluation_metric_specs_summary(items)
    out = [
        f"Valid: {summary['valid']}",
        f"Count: {summary['count']}",
        f"Kinds: {', '.join(summary['kinds'])}"
    ]
    if summary["errors"]:
        out.append(f"Errors: {', '.join(summary['errors'])}")
    return "\n".join(out)
