from typing import Any
import pandas

from usa_signal_bot.backtesting.analytics.phase148_models import ExposureDiagnosticResult
from usa_signal_bot.core.exceptions import ExposureDiagnosticsError

def build_exposure_diagnostics(run_id: str, exposure_df: pandas.DataFrame) -> list[ExposureDiagnosticResult]:
    raise NotImplementedError()

def calculate_average_exposure(exposure_df: pandas.DataFrame) -> float | None:
    raise NotImplementedError()

def calculate_time_in_exposure(exposure_df: pandas.DataFrame) -> float | None:
    raise NotImplementedError()

def calculate_symbol_exposure_summary(exposure_df: pandas.DataFrame) -> dict[str, Any]:
    raise NotImplementedError()

def validate_exposure_diagnostics(items: list[ExposureDiagnosticResult]) -> list[str]:
    raise NotImplementedError()

def exposure_diagnostics_summary(items: list[ExposureDiagnosticResult]) -> dict[str, Any]:
    raise NotImplementedError()

def exposure_diagnostics_to_text(items: list[ExposureDiagnosticResult], limit: int = 300) -> str:
    raise NotImplementedError()
