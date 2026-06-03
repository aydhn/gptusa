from typing import Any
import pandas

from usa_signal_bot.backtesting.analytics.phase148_models import BacktestAnalyticsInputReference
from usa_signal_bot.core.exceptions import AnalyticsInputResolverError

def build_backtest_analytics_input_references(payloads: dict[str, Any], dataframes: dict[str, pandas.DataFrame] | None = None) -> list[BacktestAnalyticsInputReference]:
    raise NotImplementedError()

def validate_equity_curve_frame(df: pandas.DataFrame) -> list[str]:
    raise NotImplementedError()

def validate_drawdown_curve_frame(df: pandas.DataFrame) -> list[str]:
    raise NotImplementedError()

def validate_simulated_fill_ledger_frame(df: pandas.DataFrame) -> list[str]:
    raise NotImplementedError()

def validate_cost_ledger_frame(df: pandas.DataFrame) -> list[str]:
    raise NotImplementedError()

def validate_exposure_timeline_frame(df: pandas.DataFrame) -> list[str]:
    raise NotImplementedError()

def detect_forbidden_backtest_analytics_columns(columns: list[str]) -> list[str]:
    raise NotImplementedError()

def analytics_input_resolver_summary(items: list[BacktestAnalyticsInputReference]) -> dict[str, Any]:
    raise NotImplementedError()

def analytics_input_resolver_to_text(items: list[BacktestAnalyticsInputReference], limit: int = 300) -> str:
    raise NotImplementedError()
