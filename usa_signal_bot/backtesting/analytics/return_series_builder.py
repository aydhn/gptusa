from typing import Any
import pandas

from usa_signal_bot.backtesting.analytics.phase148_models import ReturnSeriesPoint
from usa_signal_bot.core.exceptions import ReturnSeriesBuilderError

def build_return_series(equity_curve_df: pandas.DataFrame, run_id: str) -> list[ReturnSeriesPoint]:
    raise NotImplementedError()

def compute_simple_return(current_equity: float, previous_equity: float | None) -> float | None:
    raise NotImplementedError()

def compute_log_return_approx(simple_return: float | None) -> float | None:
    raise NotImplementedError()

def validate_return_series(items: list[ReturnSeriesPoint]) -> list[str]:
    raise NotImplementedError()

def return_series_to_dataframe(items: list[ReturnSeriesPoint]) -> pandas.DataFrame:
    raise NotImplementedError()

def return_series_summary(items: list[ReturnSeriesPoint]) -> dict[str, Any]:
    raise NotImplementedError()
