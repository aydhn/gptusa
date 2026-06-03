from typing import Any
from pathlib import Path

from usa_signal_bot.backtesting.analytics.phase148_models import (
    BacktestRunIngestionResult,
    create_backtest_run_ingestion_id
)
from usa_signal_bot.core.exceptions import BacktestRunIngestionError

def ingest_backtest_run_review_payload(payload: dict[str, Any]) -> BacktestRunIngestionResult:
    raise NotImplementedError()

def ingest_latest_backtest_run_review_from_store(data_root: Path) -> BacktestRunIngestionResult:
    raise NotImplementedError()

def extract_backtest_run_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    raise NotImplementedError()

def extract_backtest_run_artifact(payload: dict[str, Any]) -> dict[str, Any] | None:
    raise NotImplementedError()

def extract_backtest_run_validation_gate(payload: dict[str, Any]) -> dict[str, Any] | None:
    raise NotImplementedError()

def extract_backtest_run_safety_boundary(payload: dict[str, Any]) -> dict[str, Any] | None:
    raise NotImplementedError()

def extract_basic_performance_summary(payload: dict[str, Any]) -> dict[str, Any] | None:
    raise NotImplementedError()

def backtest_run_supports_phase148(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    raise NotImplementedError()

def backtest_run_ingestion_to_text(result: BacktestRunIngestionResult) -> str:
    raise NotImplementedError()
