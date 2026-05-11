from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from typing import Dict, Any, List, Optional
import uuid

from usa_signal_bot.core.enums import RunLockScope, IdempotencyStatus
from usa_signal_bot.scheduler.scheduler_models import IdempotencyRecord

@dataclass
class DuplicateRunCheckResult:
    check_id: str
    created_at_utc: str
    scope: RunLockScope
    duplicate: bool
    idempotency_key: Optional[str]
    matching_record: Optional[IdempotencyRecord]
    status: IdempotencyStatus
    message: str
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def build_run_payload_checksum(payload: Dict[str, Any]) -> str:
    # Filter out volatile fields like run_id, timestamp
    filtered = {}
    for k, v in payload.items():
        if k not in ["run_id", "timestamp", "created_at_utc", "heartbeat_at_utc"]:
            filtered[k] = v

    encoded = json.dumps(filtered, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

def build_idempotency_key(scope: RunLockScope, payload: Dict[str, Any]) -> str:
    checksum = build_run_payload_checksum(payload)
    return f"{scope.value.lower()}_{checksum}"

def check_duplicate_run(records: List[IdempotencyRecord], scope: RunLockScope, payload: Dict[str, Any]) -> DuplicateRunCheckResult:
    now_utc = datetime.now(timezone.utc).isoformat()
    check_id = f"dup_check_{uuid.uuid4().hex[:8]}"

    checksum = build_run_payload_checksum(payload)
    key = build_idempotency_key(scope, payload)

    for r in records:
        if r.key == key:
            status = r.status
            if status == IdempotencyStatus.COMPLETED_BEFORE or status == IdempotencyStatus.IN_PROGRESS:
                return DuplicateRunCheckResult(
                    check_id=check_id,
                    created_at_utc=now_utc,
                    scope=scope,
                    duplicate=True,
                    idempotency_key=key,
                    matching_record=r,
                    status=IdempotencyStatus.DUPLICATE,
                    message=f"Duplicate run detected. Previous status: {status.value}"
                )

    return DuplicateRunCheckResult(
        check_id=check_id,
        created_at_utc=now_utc,
        scope=scope,
        duplicate=False,
        idempotency_key=key,
        matching_record=None,
        status=IdempotencyStatus.NEW,
        message="New unique run"
    )

def duplicate_run_check_result_to_dict(result: DuplicateRunCheckResult) -> dict:
    return {
        "check_id": result.check_id,
        "created_at_utc": result.created_at_utc,
        "scope": result.scope.value,
        "duplicate": result.duplicate,
        "idempotency_key": result.idempotency_key,
        "status": result.status.value,
        "message": result.message,
        "warnings": result.warnings,
        "errors": result.errors
    }

def duplicate_run_check_result_to_text(result: DuplicateRunCheckResult) -> str:
    return f"DuplicateCheck ({result.scope.value}): {'DUPLICATE' if result.duplicate else 'NEW'} | Key: {result.idempotency_key} | {result.message}"
