from typing import Any

from usa_signal_bot.backtesting.analytics.phase148_models import DeterminismValidationResult
from usa_signal_bot.core.exceptions import DeterminismValidationError

def build_determinism_validation(run_id: str, run_artifact_payload: dict[str, Any], ledger_payload: dict[str, Any] | None = None) -> DeterminismValidationResult:
    raise NotImplementedError()

def recompute_hash_from_payload(payload: dict[str, Any]) -> str:
    raise NotImplementedError()

def compare_hashes(expected: str | None, observed: str | None) -> bool:
    raise NotImplementedError()

def validate_determinism_validation(item: DeterminismValidationResult) -> list[str]:
    raise NotImplementedError()

def determinism_validation_summary(item: DeterminismValidationResult) -> dict[str, Any]:
    raise NotImplementedError()

def determinism_validation_to_text(item: DeterminismValidationResult, limit: int = 300) -> str:
    raise NotImplementedError()
