from typing import Any
import pandas

from usa_signal_bot.backtesting.analytics.phase148_models import TradeDiagnosticRecord
from usa_signal_bot.core.exceptions import TradeDiagnosticsError

def build_trade_diagnostics(run_id: str, fill_df: pandas.DataFrame, equity_df: pandas.DataFrame | None = None) -> list[TradeDiagnosticRecord]:
    raise NotImplementedError()

def calculate_trade_count(fill_df: pandas.DataFrame) -> int:
    raise NotImplementedError()

def calculate_win_loss_count(fill_df: pandas.DataFrame) -> dict[str, int]:
    raise NotImplementedError()

def calculate_average_simulated_trade_return(fill_df: pandas.DataFrame) -> float | None:
    raise NotImplementedError()

def calculate_symbol_concentration(fill_df: pandas.DataFrame) -> dict[str, Any]:
    raise NotImplementedError()

def validate_trade_diagnostics(items: list[TradeDiagnosticRecord]) -> list[str]:
    raise NotImplementedError()

def trade_diagnostics_summary(items: list[TradeDiagnosticRecord]) -> dict[str, Any]:
    raise NotImplementedError()

def trade_diagnostics_to_text(items: list[TradeDiagnosticRecord], limit: int = 300) -> str:
    raise NotImplementedError()
