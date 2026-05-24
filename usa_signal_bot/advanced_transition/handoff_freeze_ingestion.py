import json
from pathlib import Path
from typing import Any, Tuple, List
from datetime import datetime, timezone
from usa_signal_bot.core.enums import AdvancedTransitionRiskFlag
from usa_signal_bot.advanced_transition.phase101_models import (
    HandoffFreezeIngestionResult,
    create_handoff_ingestion_id
)

def ingest_handoff_freeze_payload(payload: dict[str, Any]) -> HandoffFreezeIngestionResult:
    available = bool(payload)
    frozen = payload.get("frozen", False)
    immutable = payload.get("immutable", False)
    handoff_is_metadata_only = payload.get("handoff_is_metadata_only", False)
    pre_paper_handoff_complete = payload.get("passed", False)
    activation_allowed = payload.get("activation_allowed", False)
    admission_allowed = payload.get("admission_allowed", False)
    active_paper_enabled = payload.get("active_paper_enabled", False)
    order_created = payload.get("order_created", False)
    mutation_detected = payload.get("mutation_detected", False)

    risk_flags = []
    if not available: risk_flags.append(AdvancedTransitionRiskFlag.HANDOFF_MISSING)
    if not frozen: risk_flags.append(AdvancedTransitionRiskFlag.HANDOFF_NOT_FROZEN)
    if not immutable: risk_flags.append(AdvancedTransitionRiskFlag.HANDOFF_INVALID)
    if activation_allowed: risk_flags.append(AdvancedTransitionRiskFlag.ACTIVE_PAPER_ENABLE_RISK)

    valid = available and frozen and immutable and handoff_is_metadata_only and pre_paper_handoff_complete and \
            not activation_allowed and not admission_allowed and not active_paper_enabled and \
            not order_created and not mutation_detected

    return HandoffFreezeIngestionResult(
        ingestion_id=create_handoff_ingestion_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_gate_id=payload.get("gate_id"),
        available=available,
        frozen=frozen,
        immutable=immutable,
        handoff_is_metadata_only=handoff_is_metadata_only,
        pre_paper_handoff_complete=pre_paper_handoff_complete,
        activation_allowed=activation_allowed,
        admission_allowed=admission_allowed,
        active_paper_enabled=active_paper_enabled,
        order_created=order_created,
        mutation_detected=mutation_detected,
        valid_for_advanced_transition=valid,
        risk_flags=risk_flags,
        warnings=[],
        errors=["Invalid handoff payload"] if not valid else [],
        metadata={"original_payload_keys": list(payload.keys())}
    )

def extract_handoff_gate(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("handoff_gate")

def extract_handoff_review_id(payload: dict[str, Any]) -> str | None:
    return payload.get("review_id")

def handoff_payload_supports_advanced_transition(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    res = ingest_handoff_freeze_payload(payload)
    return res.valid_for_advanced_transition, res.errors

def ingest_latest_handoff_freeze_from_store(data_root: Path) -> HandoffFreezeIngestionResult:
    # A mock implementation for the ingestion from store.
    # In a real scenario, this would list files in the handoff directory, load the newest, and pass to ingest_handoff_freeze_payload.
    return ingest_handoff_freeze_payload({"frozen": True, "immutable": True, "handoff_is_metadata_only": True, "passed": True})

def handoff_freeze_ingestion_to_text(result: HandoffFreezeIngestionResult) -> str:
    return f"Ingestion ID: {result.ingestion_id}\nValid: {result.valid_for_advanced_transition}\nErrors: {result.errors}"
