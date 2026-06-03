from typing import Any
import pandas

from usa_signal_bot.backtesting.analytics.phase148_models import (
    ReturnSeriesPoint,
    RollingAnalyticsPoint
)
from usa_signal_bot.core.exceptions import RollingAnalyticsError

def build_rolling_analytics(return_series: list[ReturnSeriesPoint], drawdown_df: pandas.DataFrame | None = None, cost_df: pandas.DataFrame | None = None, fill_df: pandas.DataFrame | None = None, exposure_df: pandas.DataFrame | None = None, windows: list[int] | None = None) -> list[RollingAnalyticsPoint]:
    raise NotImplementedError()

def calculate_rolling_return(values: list[float]) -> float | None:
    raise NotImplementedError()

def calculate_rolling_volatility(values: list[float]) -> float | None:
    raise NotImplementedError()

def calculate_rolling_drawdown(values: list[float]) -> float | None:
    raise NotImplementedError()

def validate_rolling_analytics(items: list[RollingAnalyticsPoint]) -> list[str]:
    raise NotImplementedError()

def rolling_analytics_to_dataframe(items: list[RollingAnalyticsPoint]) -> pandas.DataFrame:
    raise NotImplementedError()

def rolling_analytics_summary(items: list[RollingAnalyticsPoint]) -> dict[str, Any]:
    raise NotImplementedError()
