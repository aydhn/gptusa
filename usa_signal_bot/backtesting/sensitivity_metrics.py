import statistics
from dataclasses import dataclass
from typing import Any
from usa_signal_bot.core.enums import SensitivityMetricName, StabilityBucket, OverfitRiskHint
from usa_signal_bot.backtesting.parameter_sensitivity_models import SensitivityCellResult, SensitivityCellStatus

@dataclass
class SensitivityAggregateMetrics:
    completed_cells: int
    failed_cells: int
    skipped_cells: int
    primary_metric: SensitivityMetricName
    primary_metric_mean: float | None
    primary_metric_median: float | None
    primary_metric_min: float | None
    primary_metric_max: float | None
    primary_metric_range: float | None
    primary_metric_std_like: float | None
    stability_score: float | None
    fragility_score: float | None
    robust_cell_ratio: float | None
    fragile_cell_ratio: float | None
    warnings: list[str]
    errors: list[str]

def extract_cell_metric(result: SensitivityCellResult, metric_name: SensitivityMetricName) -> float | None:
    metric_key_map = {
        SensitivityMetricName.RETURN_PCT: "total_return_pct",
        SensitivityMetricName.MAX_DRAWDOWN_PCT: "max_drawdown_pct",
        SensitivityMetricName.WIN_RATE: "win_rate",
        SensitivityMetricName.PROFIT_FACTOR: "profit_factor",
        SensitivityMetricName.SHARPE_LIKE: "sharpe_ratio",
    }
    key = metric_key_map.get(metric_name)
    if key and key in result.metrics:
        val = result.metrics[key]
        if isinstance(val, (int, float)):
            return float(val)
    return None

def calculate_std_like(values: list[float]) -> float | None:
    if len(values) < 2:
        return None
    return statistics.stdev(values)

def calculate_stability_score_from_values(values: list[float]) -> float | None:
    if not values:
        return None

    std = calculate_std_like(values)
    if std is None or std == 0:
        return 100.0

    mean = statistics.mean(values)
    if mean == 0:
        return 50.0

    cv = abs(std / mean)
    # Simple score mapping: lower cv -> higher score
    score = max(0.0, 100.0 - (cv * 50.0))
    return min(100.0, score)

def calculate_fragility_score_from_values(values: list[float]) -> float | None:
    stability = calculate_stability_score_from_values(values)
    if stability is None:
        return None
    return 100.0 - stability

def calculate_robust_cell_ratio(results: list[SensitivityCellResult], metric_name: SensitivityMetricName, threshold: float) -> float | None:
    completed = [r for r in results if r.status == SensitivityCellStatus.COMPLETED]
    if not completed:
        return None

    robust_count = 0
    for r in completed:
        val = extract_cell_metric(r, metric_name)
        if val is not None and val >= threshold:
            robust_count += 1

    return robust_count / len(completed)

def calculate_fragile_cell_ratio(results: list[SensitivityCellResult], metric_name: SensitivityMetricName, threshold: float) -> float | None:
    completed = [r for r in results if r.status == SensitivityCellStatus.COMPLETED]
    if not completed:
        return None

    fragile_count = 0
    for r in completed:
        val = extract_cell_metric(r, metric_name)
        if val is not None and val < threshold:
            fragile_count += 1

    return fragile_count / len(completed)

def calculate_sensitivity_aggregate_metrics(results: list[SensitivityCellResult], primary_metric: SensitivityMetricName) -> SensitivityAggregateMetrics:
    completed_cells = sum(1 for r in results if r.status == SensitivityCellStatus.COMPLETED)
    failed_cells = sum(1 for r in results if r.status == SensitivityCellStatus.FAILED)
    skipped_cells = sum(1 for r in results if r.status == SensitivityCellStatus.SKIPPED)

    values = []
    for r in results:
        if r.status == SensitivityCellStatus.COMPLETED:
            val = extract_cell_metric(r, primary_metric)
            if val is not None:
                values.append(val)

    if not values:
        return SensitivityAggregateMetrics(
            completed_cells=completed_cells, failed_cells=failed_cells, skipped_cells=skipped_cells,
            primary_metric=primary_metric, primary_metric_mean=None, primary_metric_median=None,
            primary_metric_min=None, primary_metric_max=None, primary_metric_range=None,
            primary_metric_std_like=None, stability_score=None, fragility_score=None,
            robust_cell_ratio=None, fragile_cell_ratio=None,
            warnings=["No completed cells with primary metric."], errors=[]
        )

    mean_val = statistics.mean(values)
    median_val = statistics.median(values)
    min_val = min(values)
    max_val = max(values)
    range_val = max_val - min_val
    std_val = calculate_std_like(values)
    stability = calculate_stability_score_from_values(values)
    fragility = calculate_fragility_score_from_values(values)

    threshold = median_val if median_val is not None else 0.0
    robust_ratio = calculate_robust_cell_ratio(results, primary_metric, threshold)
    fragile_ratio = calculate_fragile_cell_ratio(results, primary_metric, threshold)

    return SensitivityAggregateMetrics(
        completed_cells=completed_cells, failed_cells=failed_cells, skipped_cells=skipped_cells,
        primary_metric=primary_metric, primary_metric_mean=mean_val, primary_metric_median=median_val,
        primary_metric_min=min_val, primary_metric_max=max_val, primary_metric_range=range_val,
        primary_metric_std_like=std_val, stability_score=stability, fragility_score=fragility,
        robust_cell_ratio=robust_ratio, fragile_cell_ratio=fragile_ratio,
        warnings=[], errors=[]
    )

def classify_stability_bucket(score: float | None, completed_cells: int) -> StabilityBucket:
    if score is None or completed_cells < 2:
        return StabilityBucket.INSUFFICIENT_DATA
    if score >= 80:
        return StabilityBucket.VERY_STABLE
    if score >= 60:
        return StabilityBucket.STABLE
    if score >= 40:
        return StabilityBucket.MODERATE
    if score >= 20:
        return StabilityBucket.FRAGILE
    return StabilityBucket.VERY_FRAGILE

def classify_overfit_risk_hint(metrics: SensitivityAggregateMetrics) -> OverfitRiskHint:
    if metrics.completed_cells < 2 or metrics.stability_score is None:
        return OverfitRiskHint.INSUFFICIENT_DATA

    if metrics.stability_score < 30:
        return OverfitRiskHint.HIGH

    if metrics.primary_metric_max is not None and metrics.primary_metric_median is not None:
        if metrics.primary_metric_median > 0 and metrics.primary_metric_max > metrics.primary_metric_median * 3:
            return OverfitRiskHint.HIGH

    if metrics.stability_score > 70:
        return OverfitRiskHint.LOW

    return OverfitRiskHint.MODERATE

def sensitivity_aggregate_metrics_to_dict(metrics: SensitivityAggregateMetrics) -> dict:
    return {
        "completed_cells": metrics.completed_cells,
        "failed_cells": metrics.failed_cells,
        "skipped_cells": metrics.skipped_cells,
        "primary_metric": metrics.primary_metric.value,
        "primary_metric_mean": metrics.primary_metric_mean,
        "primary_metric_median": metrics.primary_metric_median,
        "primary_metric_min": metrics.primary_metric_min,
        "primary_metric_max": metrics.primary_metric_max,
        "primary_metric_range": metrics.primary_metric_range,
        "primary_metric_std_like": metrics.primary_metric_std_like,
        "stability_score": metrics.stability_score,
        "fragility_score": metrics.fragility_score,
        "robust_cell_ratio": metrics.robust_cell_ratio,
        "fragile_cell_ratio": metrics.fragile_cell_ratio,
        "warnings": metrics.warnings,
        "errors": metrics.errors
    }

def sensitivity_aggregate_metrics_to_text(metrics: SensitivityAggregateMetrics) -> str:
    lines = [
        "--- Sensitivity Aggregate Metrics ---",
        f"Cells: {metrics.completed_cells} completed, {metrics.failed_cells} failed, {metrics.skipped_cells} skipped",
        f"Primary Metric: {metrics.primary_metric.value}",
        f"Mean: {metrics.primary_metric_mean}, Median: {metrics.primary_metric_median}",
        f"Range: [{metrics.primary_metric_min}, {metrics.primary_metric_max}]",
        f"Stability Score: {metrics.stability_score}, Fragility Score: {metrics.fragility_score}"
    ]
    return "\n".join(lines)
