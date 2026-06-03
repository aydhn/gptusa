import math
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import TemporalStabilityMetricKind, WalkForwardRiskFlag
from usa_signal_bot.backtesting.walk_forward.phase150_models import (
    FoldPerformanceMetric,
    FoldBenchmarkComparison,
    TemporalStabilityMetric,
    create_temporal_stability_metric_id,
    _now_utc
)

def calculate_metric_stability(values: List[float]) -> Optional[float]:
    if not values or len(values) < 2:
        return None
    # Calculate simple relative standard deviation (coefficient of variation)
    mean = sum(values) / len(values)
    if mean == 0:
        return 0.0

    variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
    std = math.sqrt(variance)
    return std / abs(mean)

def infer_stability_label(value: Optional[float]) -> str:
    if value is None:
        return "UNKNOWN"
    if value < 0.1:
        return "HIGHLY_STABLE"
    if value < 0.3:
        return "STABLE"
    if value < 0.6:
        return "MODERATE"
    return "UNSTABLE"

def build_temporal_stability_metrics(fold_metrics: List[FoldPerformanceMetric], fold_comparisons: List[FoldBenchmarkComparison]) -> List[TemporalStabilityMetric]:
    metrics = []

    # We will compute a simple "return stability" across folds
    returns = [m.oos_value for m in fold_metrics if isinstance(m.oos_value, (int, float))]
    ret_stability_val = calculate_metric_stability(returns)
    ret_stability_label = infer_stability_label(ret_stability_val)

    metric = TemporalStabilityMetric(
        metric_id=create_temporal_stability_metric_id(),
        created_at_utc=_now_utc(),
        metric_kind=TemporalStabilityMetricKind.RETURN_STABILITY,
        metric_name="OOS Return Stability",
        value=ret_stability_val,
        stability_label=ret_stability_label,
        sample_count=len(returns),
        non_trading_metric=True,
        not_investment_advice=True,
        not_strategy_activation=True,
        research_data_only=True
    )

    errors = validate_temporal_stability_metrics([metric])
    if errors:
        metric.errors = errors
        metric.risk_flags.append(WalkForwardRiskFlag.TEMPORAL_STABILITY_INVALID)

    metrics.append(metric)
    return metrics

def validate_temporal_stability_metrics(items: List[TemporalStabilityMetric]) -> List[str]:
    errors = []
    for m in items:
        if not m.non_trading_metric:
            errors.append(f"Metric {m.metric_id} must be non_trading_metric")
        if not m.not_investment_advice:
            errors.append(f"Metric {m.metric_id} must be not_investment_advice")
        if not m.not_strategy_activation:
            errors.append(f"Metric {m.metric_id} must be not_strategy_activation")
    return errors

def temporal_stability_summary(items: List[TemporalStabilityMetric]) -> Dict[str, Any]:
    valid_count = sum(1 for m in items if not m.errors)
    return {
        "total_metrics": len(items),
        "valid_metrics": valid_count,
        "all_valid": valid_count == len(items) and len(items) > 0
    }

def temporal_stability_to_text(items: List[TemporalStabilityMetric], limit: int = 300) -> str:
    summary = temporal_stability_summary(items)
    return f"Temporal Stability: {summary['valid_metrics']}/{summary['total_metrics']} valid"
