import json
from pathlib import Path
from typing import Dict, Any, Dict, List, Optional

from usa_signal_bot.notifications.notification_models import (
    NotificationMessage,
    QueuedNotification,
    NotificationDispatchResult,
    notification_message_to_dict,
    notification_dispatch_result_to_dict
)
from usa_signal_bot.notifications.notification_queue import queued_notifications_to_jsonl
from usa_signal_bot.notifications.notification_validation import NotificationValidationReport

def notification_store_dir(data_root: Path) -> Path:
    d = data_root / "notifications"
    d.mkdir(parents=True, exist_ok=True)
    return d

def build_notification_run_dir(data_root: Path, dispatch_id: str) -> Path:
    if ".." in dispatch_id or "/" in dispatch_id:
        raise ValueError("Invalid dispatch_id path traversal")
    d = notification_store_dir(data_root) / dispatch_id
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_notification_messages_jsonl(path: Path, messages: List[NotificationMessage]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for msg in messages:
            f.write(json.dumps(notification_message_to_dict(msg)) + "\n")
    return path

def write_queued_notifications_jsonl(path: Path, items: List[QueuedNotification]) -> Path:
    return queued_notifications_to_jsonl(path, items)

def write_notification_dispatch_result_json(path: Path, result: NotificationDispatchResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(notification_dispatch_result_to_dict(result), f, indent=2)
    return path

def write_send_results_jsonl(path: Path, results: List[Dict[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
    return path

def write_notification_validation_report_json(path: Path, report: NotificationValidationReport) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "valid": report.valid,
        "issue_count": report.issue_count,
        "warning_count": report.warning_count,
        "error_count": report.error_count,
        "issues": [{"severity": i.severity, "field": i.field, "message": i.message} for i in report.issues]
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return path

def read_notification_messages_jsonl(path: Path) -> List[Dict[str, Any]]:
    messages = []
    if not path.exists():
        return messages
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                messages.append(json.loads(line))
    return messages

def read_notification_dispatch_result_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_notification_runs(data_root: Path) -> List[Path]:
    base_dir = notification_store_dir(data_root)
    if not base_dir.exists():
        return []
    runs = [d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith("dispatch_")]
    # sort by name desc (time desc if prefix is used)
    runs.sort(key=lambda x: x.name, reverse=True)
    return runs

def get_latest_notification_run_dir(data_root: Path) -> Optional[Path]:
    runs = list_notification_runs(data_root)
    return runs[0] if runs else None

def notification_store_summary(data_root: Path) -> Dict[str, Any]:
    runs = list_notification_runs(data_root)
    return {
        "total_runs": len(runs),
        "latest_run": runs[0].name if runs else None
    }
