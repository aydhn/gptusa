from typing import Any
from pathlib import Path
from datetime import datetime, timezone

from usa_signal_bot.advanced_runtime.phase102_models import (
    TransitionReviewIngestionResult,
    create_transition_review_ingestion_id,
    RuntimeRegistryRiskFlag
)
from usa_signal_bot.core.enums import RuntimeRegistryRiskFlag

def ingest_advanced_transition_review_payload(payload: dict[str, Any]) -> TransitionReviewIngestionResult:
    review_id = payload.get("review_id")
    if not review_id:
        return _build_invalid_ingestion(
            source_path=None,
            source_review_id=None,
            reason="Missing review_id in payload"
        )

    context = extract_advanced_transition_context(payload)
    if not context:
         return _build_invalid_ingestion(
            source_path=None,
            source_review_id=review_id,
            reason="Missing advanced transition context"
        )

    valid, errors = transition_review_supports_phase102(payload)
    risk_flags = []
    if not valid:
         risk_flags.append(RuntimeRegistryRiskFlag.TRANSITION_REVIEW_INVALID)

    return TransitionReviewIngestionResult(
        ingestion_id=create_transition_review_ingestion_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source_path=None,
        source_review_id=review_id,
        available=True,
        advanced_transition_ready=context.get("status") == "VALIDATED",
        current_phase=102,
        final_phase=160,
        activation_allowed=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        scraping_enabled=False,
        dashboard_enabled=False,
        valid_for_phase102=valid,
        risk_flags=risk_flags,
        warnings=[],
        errors=errors,
        metadata={"ingested_keys": list(payload.keys())}
    )

def ingest_latest_advanced_transition_review_from_store(data_root: Path) -> TransitionReviewIngestionResult:
    import json
    reviews_dir = data_root / "advanced_transition" / "reviews"
    if not reviews_dir.exists():
        return _build_invalid_ingestion(source_path=str(reviews_dir), source_review_id=None, reason="Reviews dir not found")

    files = list(reviews_dir.glob("*.json"))
    if not files:
        return _build_invalid_ingestion(source_path=str(reviews_dir), source_review_id=None, reason="No review files found")

    latest_file = max(files, key=lambda f: f.stat().st_mtime)
    try:
        with open(latest_file, "r") as f:
            payload = json.load(f)
            res = ingest_advanced_transition_review_payload(payload)
            res.source_path = str(latest_file)
            return res
    except Exception as e:
        return _build_invalid_ingestion(source_path=str(latest_file), source_review_id=None, reason=str(e))

def _build_invalid_ingestion(source_path: str | None, source_review_id: str | None, reason: str) -> TransitionReviewIngestionResult:
    return TransitionReviewIngestionResult(
        ingestion_id=create_transition_review_ingestion_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source_path=source_path,
        source_review_id=source_review_id,
        available=False,
        advanced_transition_ready=False,
        current_phase=102,
        final_phase=160,
        activation_allowed=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        scraping_enabled=False,
        dashboard_enabled=False,
        valid_for_phase102=False,
        risk_flags=[RuntimeRegistryRiskFlag.TRANSITION_REVIEW_MISSING],
        warnings=[],
        errors=[reason],
        metadata={}
    )

def extract_advanced_transition_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("context")

def extract_runtime_boundary_manifest(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("runtime_boundary_manifest")

def transition_review_supports_phase102(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    errors = []
    context = extract_advanced_transition_context(payload)
    if not context:
        return False, ["Missing transition context"]

    if context.get("activation_allowed"):
        errors.append("activation_allowed is true")
    if context.get("active_paper_enabled"):
        errors.append("active_paper_enabled is true")
    if context.get("broker_execution_enabled"):
        errors.append("broker_execution_enabled is true")
    if context.get("paper_state_mutation_enabled"):
        errors.append("paper_state_mutation_enabled is true")
    if context.get("telegram_real_send_enabled"):
        errors.append("telegram_real_send_enabled is true")

    return len(errors) == 0, errors

def transition_review_ingestion_to_text(result: TransitionReviewIngestionResult) -> str:
    lines = [
        f"--- Transition Review Ingestion Result ---",
        f"ID: {result.ingestion_id}",
        f"Source Review ID: {result.source_review_id}",
        f"Available: {result.available}",
        f"Advanced Transition Ready: {result.advanced_transition_ready}",
        f"Valid for Phase 102: {result.valid_for_phase102}",
        f"Errors: {len(result.errors)}"
    ]
    return "\n".join(lines)
