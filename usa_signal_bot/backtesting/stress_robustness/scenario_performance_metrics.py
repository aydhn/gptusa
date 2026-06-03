import datetime
from typing import Any

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    ScenarioReplayResult,
    ScenarioPerformanceMetric,
    create_scenario_performance_metric_id
)
from usa_signal_bot.core.enums import StressMetricKind

def build_scenario_performance_metrics(results: list[ScenarioReplayResult], baseline_total_return: float | None = None) -> list[ScenarioPerformanceMetric]:
    metrics = []

    for r in results:
        # Total Return
        metrics.append(ScenarioPerformanceMetric(
            metric_id=create_scenario_performance_metric_id(),
            created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
            scenario_id=r.scenario_id,
            scenario_kind=r.scenario_kind,
            severity_level=r.severity_level,
            metric_kind=StressMetricKind.STRESSED_TOTAL_RETURN,
            metric_name="Stressed Total Return",
            value=r.stressed_total_return,
            baseline_value=baseline_total_return,
            degradation_value=calculate_scenario_degradation(r.stressed_total_return, baseline_total_return),
            non_trading_metric=True,
            not_investment_advice=True,
            not_strategy_activation=True,
            research_data_only=True,
            warnings=[], errors=[], risk_flags=[], metadata={}
        ))

        # Max Drawdown
        metrics.append(ScenarioPerformanceMetric(
            metric_id=create_scenario_performance_metric_id(),
            created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
            scenario_id=r.scenario_id,
            scenario_kind=r.scenario_kind,
            severity_level=r.severity_level,
            metric_kind=StressMetricKind.STRESSED_MAX_DRAWDOWN,
            metric_name="Stressed Max Drawdown",
            value=r.stressed_max_drawdown,
            baseline_value=None,
            degradation_value=None,
            non_trading_metric=True,
            not_investment_advice=True,
            not_strategy_activation=True,
            research_data_only=True,
            warnings=[], errors=[], risk_flags=[], metadata={}
        ))

    return metrics

def calculate_scenario_degradation(value: float | None, baseline_value: float | None) -> float | None:
    if value is None or baseline_value is None:
        return None
    return value - baseline_value
