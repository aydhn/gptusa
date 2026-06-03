import math
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import WalkForwardRiskFlag
from usa_signal_bot.backtesting.walk_forward.phase150_models import (
    FoldPerformanceMetric,
    FoldBenchmarkComparison,
    OOSRobustnessMetrics,
    create_oos_robustness_metrics_id,
    _now_utc
)

def calculate_fold_pass_rate(fold_metrics: List[FoldPerformanceMetric]) -> Optional[float]:
    if not fold_metrics:
        return None

    # In a real impl, we'd have a pass/fail criteria per fold.
    # We mock this by saying anything with a degradation value > -0.5 passed.
    passed = sum(1 for m in fold_metrics if m.degradation_value is not None and m.degradation_value > -0.5)
    return passed / len(fold_metrics)

def calculate_robustness_score(metrics: OOSRobustnessMetrics) -> Optional[float]:
    if metrics.fold_pass_rate is None or metrics.oos_return_mean is None:
        return None

    # A simple combined score (example)
    score = (metrics.fold_pass_rate * 50) + (metrics.oos_return_mean * 100)
    return min(100.0, max(0.0, score))

def build_oos_robustness_metrics(fold_metrics: List[FoldPerformanceMetric], fold_comparisons: List[FoldBenchmarkComparison]) -> OOSRobustnessMetrics:
    pass_rate = calculate_fold_pass_rate(fold_metrics)
    passed_folds = int(pass_rate * len(fold_metrics)) if pass_rate is not None else 0
    failed_folds = len(fold_metrics) - passed_folds

    returns = [m.oos_value for m in fold_metrics if isinstance(m.oos_value, (int, float))]

    mean_ret = sum(returns) / len(returns) if returns else 0.0
    min_ret = min(returns) if returns else 0.0
    max_ret = max(returns) if returns else 0.0

    sorted_ret = sorted(returns)
    med_ret = sorted_ret[len(sorted_ret)//2] if returns else 0.0

    std_ret = 0.0
    if len(returns) > 1:
        variance = sum((x - mean_ret) ** 2 for x in returns) / (len(returns) - 1)
        std_ret = math.sqrt(variance)

    metrics = OOSRobustnessMetrics(
        metrics_id=create_oos_robustness_metrics_id(),
        created_at_utc=_now_utc(),
        fold_count=len(fold_metrics),
        passed_fold_count=passed_folds,
        failed_fold_count=failed_folds,
        oos_return_mean=mean_ret,
        oos_return_median=med_ret,
        oos_return_min=min_ret,
        oos_return_max=max_ret,
        oos_return_std=std_ret,
        oos_max_drawdown_mean=0.05, # Mock
        oos_excess_return_mean=0.01, # Mock
        oos_cost_drag_mean=0.001, # Mock
        fold_pass_rate=pass_rate,
        robustness_score=None,
        metrics_valid=True,
        non_trading_metric=True,
        not_investment_advice=True,
        not_strategy_activation=True,
        research_data_only=True
    )

    metrics.robustness_score = calculate_robustness_score(metrics)

    errors = validate_oos_robustness_metrics(metrics)
    if errors:
        metrics.metrics_valid = False
        metrics.errors = errors
        metrics.risk_flags.append(WalkForwardRiskFlag.OOS_ROBUSTNESS_INVALID)

    return metrics

def validate_oos_robustness_metrics(item: OOSRobustnessMetrics) -> List[str]:
    errors = []
    if not item.non_trading_metric:
        errors.append("OOS metrics must be non_trading_metric")
    if not item.not_investment_advice:
        errors.append("OOS metrics must be not_investment_advice")
    if not item.not_strategy_activation:
        errors.append("OOS metrics must be not_strategy_activation")
    return errors

def oos_robustness_metrics_summary(item: OOSRobustnessMetrics) -> Dict[str, Any]:
    return {
        "valid": item.metrics_valid,
        "fold_count": item.fold_count,
        "pass_rate": item.fold_pass_rate,
        "score": item.robustness_score
    }

def oos_robustness_metrics_to_text(item: OOSRobustnessMetrics, limit: int = 300) -> str:
    summary = oos_robustness_metrics_summary(item)
    lines = [
        f"OOS Robustness Metrics:",
        f"  Valid: {summary['valid']}",
        f"  Pass Rate: {summary['pass_rate']}",
        f"  Score: {summary['score']}"
    ]
    return "\n".join(lines)[:limit]
