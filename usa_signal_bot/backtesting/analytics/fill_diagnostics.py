from typing import Any
import pandas

from usa_signal_bot.backtesting.analytics.phase148_models import FillDiagnosticRecord
from usa_signal_bot.core.exceptions import FillDiagnosticsError

def build_fill_diagnostics(run_id: str, fill_df: pandas.DataFrame) -> list[FillDiagnosticRecord]:
    raise NotImplementedError()

def count_fill_kinds(fill_df: pandas.DataFrame) -> dict[str, int]:
    raise NotImplementedError()

def calculate_fill_notional_summary(fill_df: pandas.DataFrame) -> dict[str, Any]:
    raise NotImplementedError()

def validate_fill_diagnostics(items: list[FillDiagnosticRecord]) -> list[str]:
    raise NotImplementedError()

def fill_diagnostics_summary(items: list[FillDiagnosticRecord]) -> dict[str, Any]:
    raise NotImplementedError()

def fill_diagnostics_to_text(items: list[FillDiagnosticRecord], limit: int = 300) -> str:
    raise NotImplementedError()
