from typing import Any
import pandas

from usa_signal_bot.backtesting.analytics.phase148_models import CostDiagnosticRecord
from usa_signal_bot.core.exceptions import CostDiagnosticsError

def build_cost_diagnostics(run_id: str, cost_df: pandas.DataFrame, equity_df: pandas.DataFrame | None = None) -> list[CostDiagnosticRecord]:
    raise NotImplementedError()

def calculate_total_cost_components(cost_df: pandas.DataFrame) -> dict[str, float]:
    raise NotImplementedError()

def calculate_cost_drag_on_return(cost_df: pandas.DataFrame, equity_df: pandas.DataFrame | None = None) -> float | None:
    raise NotImplementedError()

def validate_cost_diagnostics(items: list[CostDiagnosticRecord]) -> list[str]:
    raise NotImplementedError()

def cost_diagnostics_summary(items: list[CostDiagnosticRecord]) -> dict[str, Any]:
    raise NotImplementedError()

def cost_diagnostics_to_text(items: list[CostDiagnosticRecord], limit: int = 300) -> str:
    raise NotImplementedError()
