from typing import Any

from usa_signal_bot.backtesting.analytics.phase148_models import (
    RunValidationReport,
    LedgerReconciliationResult,
    DeterminismValidationResult
)
from usa_signal_bot.core.exceptions import RunValidationReportError

def build_run_validation_report(run_id: str, ledger_reconciliation: LedgerReconciliationResult, determinism_validation: DeterminismValidationResult) -> RunValidationReport:
    raise NotImplementedError()

def compute_run_validation_report_hash(report: RunValidationReport) -> str:
    raise NotImplementedError()

def validate_run_validation_report(report: RunValidationReport) -> list[str]:
    raise NotImplementedError()

def run_validation_report_summary(report: RunValidationReport) -> dict[str, Any]:
    raise NotImplementedError()

def run_validation_report_to_text(report: RunValidationReport, limit: int = 300) -> str:
    raise NotImplementedError()
