from typing import Any
from pathlib import Path
import pandas

from usa_signal_bot.core.exceptions import BacktestRunArtifactLoaderError

def load_backtest_run_artifact_json(path: Path) -> dict[str, Any]:
    raise NotImplementedError()

def load_backtest_run_validation_gate_json(path: Path) -> dict[str, Any]:
    raise NotImplementedError()

def load_backtest_run_safety_boundary_json(path: Path) -> dict[str, Any]:
    raise NotImplementedError()

def load_basic_performance_summary_json(path: Path) -> dict[str, Any]:
    raise NotImplementedError()

def load_simulated_fill_ledger_csv(path: Path) -> pandas.DataFrame:
    raise NotImplementedError()

def load_cost_ledger_csv(path: Path) -> pandas.DataFrame:
    raise NotImplementedError()

def load_exposure_timeline_csv(path: Path) -> pandas.DataFrame:
    raise NotImplementedError()

def load_equity_curve_csv(path: Path) -> pandas.DataFrame:
    raise NotImplementedError()

def load_drawdown_curve_csv(path: Path) -> pandas.DataFrame:
    raise NotImplementedError()

def validate_backtest_run_artifacts(payloads: dict[str, Any]) -> list[str]:
    raise NotImplementedError()

def backtest_run_artifact_loader_summary(payloads: dict[str, Any]) -> dict[str, Any]:
    raise NotImplementedError()

def backtest_run_artifact_loader_to_text(payloads: dict[str, Any], limit: int = 300) -> str:
    raise NotImplementedError()
