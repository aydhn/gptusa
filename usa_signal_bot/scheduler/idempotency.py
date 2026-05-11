import json
import os
import tempfile
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional

from usa_signal_bot.core.enums import RunLockScope, IdempotencyStatus
from usa_signal_bot.scheduler.scheduler_models import IdempotencyRecord, idempotency_record_to_dict

class IdempotencyStore:
    def __init__(self, path: Path):
        self.path = path
        if not self.path.parent.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)

    def load_records(self) -> List[IdempotencyRecord]:
        if not self.path.exists():
            return []
        records = []
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        records.append(IdempotencyRecord(
                            key=data["key"],
                            run_id=data["run_id"],
                            scope=RunLockScope(data["scope"]),
                            status=IdempotencyStatus(data["status"]),
                            created_at_utc=data["created_at_utc"],
                            completed_at_utc=data.get("completed_at_utc"),
                            payload_checksum=data.get("payload_checksum"),
                            output_paths=data.get("output_paths", {}),
                            metadata=data.get("metadata", {})
                        ))
                    except Exception:
                        continue
        except Exception:
            pass
        return records

    def append_record(self, record: IdempotencyRecord) -> Path:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(idempotency_record_to_dict(record)) + "\n")
        return self.path

    def find_by_key(self, key: str) -> Optional[IdempotencyRecord]:
        records = self.load_records()
        for r in reversed(records):
            if r.key == key:
                return r
        return None

    def mark_in_progress(self, key: str, scope: RunLockScope, run_id: str, payload_checksum: Optional[str] = None) -> IdempotencyRecord:
        now_utc = datetime.now(timezone.utc).isoformat()
        record = IdempotencyRecord(
            key=key,
            run_id=run_id,
            scope=scope,
            status=IdempotencyStatus.IN_PROGRESS,
            created_at_utc=now_utc,
            payload_checksum=payload_checksum
        )
        self.append_record(record)
        return record

    def mark_completed(self, key: str, output_paths: Optional[Dict[str, str]] = None) -> Optional[IdempotencyRecord]:
        record = self.find_by_key(key)
        if not record:
            return None
        record.status = IdempotencyStatus.COMPLETED_BEFORE
        record.completed_at_utc = datetime.now(timezone.utc).isoformat()
        if output_paths:
            record.output_paths = output_paths
        self.append_record(record)
        return record

    def prune_expired(self, max_age_days: int = 30, dry_run: bool = True) -> List[IdempotencyRecord]:
        records = self.load_records()
        now = datetime.now(timezone.utc)

        retained = []
        pruned = []

        for r in records:
            try:
                dt = datetime.fromisoformat(r.created_at_utc)
                if (now - dt).days > max_age_days:
                    pruned.append(r)
                else:
                    retained.append(r)
            except Exception:
                retained.append(r)

        if not dry_run and pruned:
            fd, temp_path = tempfile.mkstemp(dir=self.path.parent, prefix="idem_tmp_", suffix=".jsonl")
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    for r in retained:
                        f.write(json.dumps(idempotency_record_to_dict(r)) + "\n")
                os.replace(temp_path, self.path)
            except Exception as e:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                raise e

        return pruned

def create_idempotency_record(key: str, scope: RunLockScope, run_id: str, status: IdempotencyStatus, payload_checksum: Optional[str] = None) -> IdempotencyRecord:
    return IdempotencyRecord(
        key=key,
        run_id=run_id,
        scope=scope,
        status=status,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        payload_checksum=payload_checksum
    )

def idempotency_records_to_text(records: List[IdempotencyRecord], limit: int = 50) -> str:
    lines = [f"Idempotency Records (Showing {min(len(records), limit)} of {len(records)})"]
    for r in reversed(records[-limit:]):
        lines.append(f" - {r.key} [{r.status.value}] at {r.created_at_utc}")
    return "\n".join(lines)
