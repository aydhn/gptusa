from typing import Any

def ingest_read_only_paper_snapshot(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return payload or {}

def extract_paper_snapshot_id(payload: dict[str, Any]) -> str | None:
    return payload.get("snapshot_id")

def extract_paper_positions_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return payload.get("positions_summary", {})

def extract_paper_signal_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return payload.get("signal_summary", {})

def validate_paper_snapshot_not_mutable(payload: dict[str, Any]) -> list[str]:
    errors = []
    if payload.get("paper_state_committed"): errors.append("paper_state_committed must be false")
    if payload.get("paper_order_executed"): errors.append("paper_order_executed must be false")
    return errors

def paper_snapshot_ingestion_to_text(payload: dict[str, Any]) -> str:
    return str(payload)
