from typing import Any
import pandas

from usa_signal_bot.backtesting.analytics.phase148_models import (
    ReturnSeriesPoint,
    AdvancedPerformanceMetricResult
)
from usa_signal_bot.core.exceptions import AdvancedPerformanceMetricsError

def calculate_advanced_performance_metrics(run_id: str, return_series: list[ReturnSeriesPoint], equity_curve_df: pandas.DataFrame, drawdown_df: pandas.DataFrame, fill_df: pandas.DataFrame, cost_df: pandas.DataFrame, exposure_df: pandas.DataFrame) -> list[AdvancedPerformanceMetricResult]:
    raise NotImplementedError()

def calculate_cagr_approx(equity_curve_df: pandas.DataFrame) -> float | None:
    raise NotImplementedError()

def calculate_volatility_annualized_approx(returns: list[float], periods_per_year: int = 252) -> float | None:
    raise NotImplementedError()

def calculate_downside_volatility_approx(returns: list[float], periods_per_year: int = 252) -> float | None:
    raise NotImplementedError()

def calculate_sharpe_like_ratio(returns: list[float]) -> float | None:
    raise NotImplementedError()

def calculate_sortino_like_ratio(returns: list[float]) -> float | None:
    raise NotImplementedError()

def calculate_calmar_like_ratio(total_return: float | None, max_drawdown: float | None) -> float | None:
    raise NotImplementedError()

def calculate_return_skew_approx(returns: list[float]) -> float | None:
    raise NotImplementedError()

def calculate_return_kurtosis_approx(returns: list[float]) -> float | None:
    raise NotImplementedError()

def calculate_profit_factor_approx(fill_df: pandas.DataFrame) -> float | None:
    raise NotImplementedError()

def calculate_trade_expectancy_approx(fill_df: pandas.DataFrame) -> float | None:
    raise NotImplementedError()

def validate_advanced_performance_metrics(items: list[AdvancedPerformanceMetricResult]) -> list[str]:
    raise NotImplementedError()

def advanced_performance_metrics_summary(items: list[AdvancedPerformanceMetricResult]) -> dict[str, Any]:
    raise NotImplementedError()

def advanced_performance_metrics_to_text(items: list[AdvancedPerformanceMetricResult], limit: int = 300) -> str:
    raise NotImplementedError()
