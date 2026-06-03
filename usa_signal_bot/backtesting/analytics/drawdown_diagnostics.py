from typing import Any
import pandas

from usa_signal_bot.backtesting.analytics.phase148_models import DrawdownDiagnosticResult
from usa_signal_bot.core.exceptions import DrawdownDiagnosticsError

def build_drawdown_diagnostics(run_id: str, drawdown_df: pandas.DataFrame) -> list[DrawdownDiagnosticResult]:
    raise NotImplementedError()

def calculate_drawdown_duration_summary(drawdown_df: pandas.DataFrame) -> dict[str, Any]:
    raise NotImplementedError()

def identify_max_drawdown_period(drawdown_df: pandas.DataFrame) -> dict[str, Any]:
    raise NotImplementedError()

def validate_drawdown_diagnostics(items: list[DrawdownDiagnosticResult]) -> list[str]:
    raise NotImplementedError()

def drawdown_diagnostics_summary(items: list[DrawdownDiagnosticResult]) -> dict[str, Any]:
    raise NotImplementedError()

def drawdown_diagnostics_to_text(items: list[DrawdownDiagnosticResult], limit: int = 300) -> str:
    raise NotImplementedError()
