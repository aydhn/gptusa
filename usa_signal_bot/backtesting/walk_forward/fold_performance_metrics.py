from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import OOSMetricKind, WalkForwardRiskFlag
from usa_signal_bot.backtesting.walk_forward.phase150_models import (
    FoldReplayResult,
    FoldPerformanceMetric,
    create_fold_performance_metric_id,
    _now_utc
)

def calculate_fold_degradation(in_sample_value: Optional[float], oos_value: Optional[float]) -> Optional[float]:
    if in_sample_value is None or oos_value is None:
        return None
    if in_sample_value == 0:
        return 0.0
    return (oos_value - in_sample_value) / abs(in_sample_value)

def build_fold_performance_metrics(fold_results: List[FoldReplayResult]) -> List[FoldPerformanceMetric]:
    metrics = []

    for res in fold_results:
        # Mock calculation of some essential OOS Metric Kinds from the dict
        # In a real system, this unpacks the res.oos_metric_values

        # OOS Total Return
        oos_ret = res.oos_metric_values.get("OOS_TOTAL_RETURN", 0.0)
        is_ret = res.train_metric_values.get("OOS_TOTAL_RETURN", 0.0)

        metric = FoldPerformanceMetric(
            metric_id=create_fold_performance_metric_id(),
            created_at_utc=_now_utc(),
            fold_id=res.fold_id,
            fold_index=res.fold_index,
            metric_kind=OOSMetricKind.OOS_TOTAL_RETURN,
            metric_name="OOS Total Return",
            in_sample_value=is_ret,
            oos_value=oos_ret,
            degradation_value=calculate_fold_degradation(is_ret, oos_ret),
            sample_count=len(res.oos_metric_values),
            non_trading_metric=True,
            not_investment_advice=True,
            not_strategy_activation=True,
            research_data_only=True
        )

        errors = validate_fold_performance_metrics([metric])
        if errors:
            metric.errors = errors
            metric.risk_flags.append(WalkForwardRiskFlag.FOLD_METRIC_INVALID)

        metrics.append(metric)
    return metrics

def validate_fold_performance_metrics(items: List[FoldPerformanceMetric]) -> List[str]:
    errors = []
    for m in items:
        if not m.non_trading_metric:
            errors.append(f"Metric {m.metric_id} must be non_trading_metric")
        if not m.not_investment_advice:
            errors.append(f"Metric {m.metric_id} must be not_investment_advice")
        if not m.not_strategy_activation:
            errors.append(f"Metric {m.metric_id} must be not_strategy_activation")
    return errors

def fold_performance_metrics_summary(items: List[FoldPerformanceMetric]) -> Dict[str, Any]:
    valid_count = sum(1 for m in items if not m.errors)
    return {
        "total_metrics": len(items),
        "valid_metrics": valid_count,
        "all_valid": valid_count == len(items) and len(items) > 0
    }

def fold_performance_metrics_to_text(items: List[FoldPerformanceMetric], limit: int = 300) -> str:
    summary = fold_performance_metrics_summary(items)
    return f"Fold Performance Metrics: {summary['valid_metrics']}/{summary['total_metrics']} valid"
