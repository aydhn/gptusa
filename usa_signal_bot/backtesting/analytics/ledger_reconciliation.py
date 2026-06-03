from typing import Any
import pandas

from usa_signal_bot.backtesting.analytics.phase148_models import (
    LedgerReconciliationResult,
    RunConsistencyCheck
)
from usa_signal_bot.core.exceptions import LedgerReconciliationError

def build_ledger_reconciliation(run_id: str, run_artifact_payload: dict[str, Any], fill_df: pandas.DataFrame, cost_df: pandas.DataFrame, exposure_df: pandas.DataFrame, equity_df: pandas.DataFrame) -> LedgerReconciliationResult:
    raise NotImplementedError()

def build_run_consistency_checks(run_id: str, run_artifact_payload: dict[str, Any], fill_df: pandas.DataFrame, cost_df: pandas.DataFrame, exposure_df: pandas.DataFrame, equity_df: pandas.DataFrame) -> list[RunConsistencyCheck]:
    raise NotImplementedError()

def check_no_real_orders(fill_df: pandas.DataFrame) -> RunConsistencyCheck:
    raise NotImplementedError()

def check_no_paper_mutation(fill_df: pandas.DataFrame) -> RunConsistencyCheck:
    raise NotImplementedError()

def check_timestamp_order(df: pandas.DataFrame, timestamp_col: str = "timestamp") -> RunConsistencyCheck:
    raise NotImplementedError()

def validate_ledger_reconciliation(item: LedgerReconciliationResult) -> list[str]:
    raise NotImplementedError()

def ledger_reconciliation_summary(item: LedgerReconciliationResult) -> dict[str, Any]:
    raise NotImplementedError()

def ledger_reconciliation_to_text(item: LedgerReconciliationResult, limit: int = 300) -> str:
    raise NotImplementedError()
