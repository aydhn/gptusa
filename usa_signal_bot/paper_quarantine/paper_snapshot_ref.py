import hashlib
import json
import datetime
from typing import Any

from usa_signal_bot.paper_quarantine.quarantine_models import (
    PaperSnapshotRef,
    create_paper_snapshot_ref_id,
    validate_paper_snapshot_ref,
)

def stable_snapshot_hash(snapshot_payload: dict[str, Any]) -> str:
    # Ensure stable sorting for hash
    serialized = json.dumps(snapshot_payload, sort_keys=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

def redact_snapshot_sensitive_fields(snapshot_payload: dict[str, Any]) -> dict[str, Any]:
    redacted = snapshot_payload.copy()
    sensitive_keys = ["api_key", "secret", "token", "password", "broker_account_id"]

    def _redact(d: dict):
        for k, v in list(d.items()):
            if any(s in k.lower() for s in sensitive_keys):
                d[k] = "[REDACTED]"
            elif isinstance(v, dict):
                _redact(v)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        _redact(item)

    _redact(redacted)
    return redacted

def build_read_only_paper_snapshot_ref(snapshot_payload: dict[str, Any] | None = None, source: str = "local_paper_snapshot") -> PaperSnapshotRef:
    payload = snapshot_payload or {}
    redacted = redact_snapshot_sensitive_fields(payload)

    summary = {
        "keys": list(redacted.keys()),
        "source": source
    }

    ref = PaperSnapshotRef(
        snapshot_ref_id=create_paper_snapshot_ref_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        source=source,
        snapshot_hash=stable_snapshot_hash(redacted) if payload else None,
        snapshot_summary=summary,
        read_only=True,
        allows_mutation=False,
        warnings=[],
        errors=[],
    )
    validate_paper_snapshot_ref(ref)
    return ref

def validate_snapshot_ref_read_only(ref: PaperSnapshotRef) -> list[str]:
    errors = []
    if not ref.read_only:
        errors.append("Snapshot must be read_only=True")
    if ref.allows_mutation:
        errors.append("Snapshot allows_mutation must be False")
    return errors

def paper_snapshot_ref_summary(ref: PaperSnapshotRef) -> dict[str, Any]:
    return {
        "id": ref.snapshot_ref_id,
        "hash": ref.snapshot_hash,
        "read_only": ref.read_only,
        "allows_mutation": ref.allows_mutation,
    }

def paper_snapshot_ref_to_text(ref: PaperSnapshotRef) -> str:
    lines = [
        f"Paper Snapshot Ref: {ref.snapshot_ref_id}",
        f"Created At: {ref.created_at_utc}",
        f"Read Only: {ref.read_only}",
        f"Allows Mutation: {ref.allows_mutation}",
        f"Hash: {ref.snapshot_hash}",
    ]
    return "\n".join(lines)
