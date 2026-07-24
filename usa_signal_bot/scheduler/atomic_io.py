import json
import os
import logging
import tempfile
import hashlib
import uuid
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from usa_signal_bot.core.enums import AtomicWriteStatus

logger = logging.getLogger(__name__)


@dataclass
class AtomicWriteResult:
    result_id: str
    created_at_utc: str
    status: AtomicWriteStatus
    target_path: str
    temp_path: Optional[str]
    bytes_written: int
    checksum: Optional[str]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def ensure_parent_dir(path: Path) -> None:
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)


def safe_replace(src: Path, dst: Path) -> AtomicWriteResult:
    result_id = f"atomic_{uuid.uuid4().hex[:8]}"
    now_utc = datetime.now(timezone.utc).isoformat()
    try:
        bytes_len = os.path.getsize(src) if src.exists() else 0
        os.replace(src, dst)
        return AtomicWriteResult(
            result_id=result_id,
            created_at_utc=now_utc,
            status=AtomicWriteStatus.REPLACED,
            target_path=str(dst),
            temp_path=str(src),
            bytes_written=bytes_len,
            checksum=None,
        )
    except Exception as e:
        return AtomicWriteResult(
            result_id=result_id,
            created_at_utc=now_utc,
            status=AtomicWriteStatus.FAILED,
            target_path=str(dst),
            temp_path=str(src),
            bytes_written=0,
            checksum=None,
            errors=[str(e)],
        )


def atomic_write_text(
    path: Path, text: str, encoding: str = "utf-8"
) -> AtomicWriteResult:
    result_id = f"atomic_{uuid.uuid4().hex[:8]}"
    now_utc = datetime.now(timezone.utc).isoformat()
    ensure_parent_dir(path)

    encoded = text.encode(encoding)
    checksum = hashlib.sha256(encoded).hexdigest()
    bytes_len = len(encoded)

    fd, temp_path = tempfile.mkstemp(
        dir=path.parent, prefix="atomic_tmp_", suffix=".txt"
    )
    try:
        with os.fdopen(fd, "w", encoding=encoding) as f:
            f.write(text)
        os.replace(temp_path, path)
        return AtomicWriteResult(
            result_id=result_id,
            created_at_utc=now_utc,
            status=AtomicWriteStatus.WRITTEN,
            target_path=str(path),
            temp_path=temp_path,
            bytes_written=bytes_len,
            checksum=checksum,
        )
    except Exception as e:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as cleanup_e:
                logger.warning(
                    f"Failed to clean up temporary file {temp_path}: {cleanup_e}"
                )
        return AtomicWriteResult(
            result_id=result_id,
            created_at_utc=now_utc,
            status=AtomicWriteStatus.FAILED,
            target_path=str(path),
            temp_path=temp_path,
            bytes_written=0,
            checksum=None,
            errors=[str(e)],
        )


def atomic_write_json(path: Path, payload: Dict[str, Any]) -> AtomicWriteResult:
    text = json.dumps(payload, indent=2)
    return atomic_write_text(path, text)


def atomic_write_jsonl(path: Path, records: List[Dict[str, Any]]) -> AtomicWriteResult:
    text = "\n".join(json.dumps(r) for r in records) + "\n"
    return atomic_write_text(path, text)


def atomic_write_result_to_dict(result: AtomicWriteResult) -> dict:
    return {
        "result_id": result.result_id,
        "created_at_utc": result.created_at_utc,
        "status": result.status.value,
        "target_path": result.target_path,
        "temp_path": result.temp_path,
        "bytes_written": result.bytes_written,
        "checksum": result.checksum,
        "warnings": result.warnings,
        "errors": result.errors,
    }


def atomic_write_result_to_text(result: AtomicWriteResult) -> str:
    return f"AtomicWrite [{result.status.value}] to {result.target_path} ({result.bytes_written} bytes)"
