import tempfile
from pathlib import Path

from usa_signal_bot.scheduler.lock_audit import (
    create_lock_audit_event, write_lock_audit_jsonl, read_lock_audit_jsonl,
    lock_audit_summary, lock_audit_summary_to_text
)
from usa_signal_bot.core.enums import RunLockScope

def test_lock_audit_event():
    evt = create_lock_audit_event("ACQUIRE", RunLockScope.SCAN, "SUCCESS", "lock1", "run1", "ok")
    assert evt.event_type == "ACQUIRE"
    assert evt.scope == RunLockScope.SCAN
    assert evt.status == "SUCCESS"

def test_write_read_lock_audit():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "audit.jsonl"
        evt = create_lock_audit_event("ACQUIRE", RunLockScope.SCAN, "SUCCESS")

        write_lock_audit_jsonl(p, [evt])
        records = read_lock_audit_jsonl(p)
        assert len(records) == 1
        assert records[0]["event_type"] == "ACQUIRE"

def test_lock_audit_summary():
    events = [
        {"event_type": "ACQUIRE", "scope": "SCAN", "status": "SUCCESS"},
        {"event_type": "RELEASE", "scope": "SCAN", "status": "SUCCESS"},
    ]
    summ = lock_audit_summary(events)
    assert summ["total_events"] == 2
    assert summ["types"]["ACQUIRE"] == 1

    txt = lock_audit_summary_to_text(summ)
    assert "Lock Audit Summary" in txt
