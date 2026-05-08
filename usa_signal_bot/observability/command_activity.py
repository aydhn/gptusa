import json
import uuid
import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from pathlib import Path
from usa_signal_bot.core.enums import OperationalMetricStatus

@dataclass
class CommandActivityRecord:
    command_id: str
    command: str
    started_at_utc: str
    completed_at_utc: Optional[str]
    duration_seconds: Optional[float]
    status: OperationalMetricStatus
    exit_code: Optional[int]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def create_command_activity_record(command: str) -> CommandActivityRecord:
    return CommandActivityRecord(
        command_id=f"cmd_{uuid.uuid4().hex[:8]}",
        command=command,
        started_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        completed_at_utc=None,
        duration_seconds=None,
        status=OperationalMetricStatus.UNKNOWN,
        exit_code=None
    )

def complete_command_activity(record: CommandActivityRecord, exit_code: int = 0,
                              warnings: Optional[List[str]] = None, errors: Optional[List[str]] = None) -> CommandActivityRecord:
    record.completed_at_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

    t0 = datetime.datetime.fromisoformat(record.started_at_utc)
    t1 = datetime.datetime.fromisoformat(record.completed_at_utc)
    record.duration_seconds = (t1 - t0).total_seconds()

    record.exit_code = exit_code
    record.status = OperationalMetricStatus.OK if exit_code == 0 else OperationalMetricStatus.CRITICAL
    if warnings: record.warnings.extend(warnings)
    if errors: record.errors.extend(errors)
    return record

def command_activity_record_to_dict(record: CommandActivityRecord) -> dict:
    from dataclasses import asdict
    return asdict(record)

def write_command_activity_jsonl(path: Path, records: List[CommandActivityRecord]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(command_activity_record_to_dict(r)) + "\n")
    return path

def read_command_activity_jsonl(path: Path, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    res = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip(): continue
            try:
                res.append(json.loads(line))
            except:
                pass
            if limit and len(res) >= limit:
                break
    return res

def summarize_command_activity(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "total": len(records),
        "success": sum(1 for r in records if r.get("exit_code") == 0),
        "failures": sum(1 for r in records if r.get("exit_code") != 0)
    }

def command_activity_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Commands run: {summary.get('total', 0)} | Success: {summary.get('success', 0)} | Failures: {summary.get('failures', 0)}"
