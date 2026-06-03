import math
import numpy as np
from typing import Any, Dict, List, Optional
import datetime
from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import RelativePerformanceMetricResult, StrategyBenchmarkAlignment, RelativePerformanceMetricKind, create_relative_performance_metric_id
def calculate_relative_performance_metrics(run_id: str, alignment: StrategyBenchmarkAlignment, cost_payload: Optional[Dict[str, Any]] = None) -> List[RelativePerformanceMetricResult]:
    results = []
    if not alignment.aligned_points: return results
    excess = alignment.aligned_points[-1].strategy_cumulative_return - alignment.aligned_points[-1].benchmark_cumulative_return if alignment.aligned_points[-1].strategy_cumulative_return is not None and alignment.aligned_points[-1].benchmark_cumulative_return is not None else None
    results.append(RelativePerformanceMetricResult(metric_id=create_relative_performance_metric_id(), created_at_utc="", run_id=run_id, benchmark_id=alignment.benchmark_id, benchmark_kind=alignment.benchmark_kind, metric_kind=RelativePerformanceMetricKind.EXCESS_TOTAL_RETURN, metric_name="Excess Total Return", value=excess))
    return results
def relative_performance_metrics_to_text(items: List[RelativePerformanceMetricResult], limit=300) -> str: return "metrics"
