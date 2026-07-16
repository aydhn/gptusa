import tempfile
from pathlib import Path

from usa_signal_bot.scheduler.lock_audit import (
    create_lock_audit_event, LockAuditRequest, write_lock_audit_jsonl, read_lock_audit_jsonl,
    lock_audit_summary, lock_audit_summary_to_text
)
from usa_signal_bot.core.enums import RunLockScope

def test_lock_audit_event():
    evt = create_lock_audit_event(LockAuditRequest(event_type="ACQUIRE", scope=RunLockScope.SCAN, status="SUCCESS", lock_id="lock1", owner_run_id="run1", message="ok"))
    assert evt.event_type == "ACQUIRE"
    assert evt.scope == RunLockScope.SCAN
    assert evt.status == "SUCCESS"

def test_write_read_lock_audit():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "audit.jsonl"
        evt = create_lock_audit_event(LockAuditRequest(event_type="ACQUIRE", scope=RunLockScope.SCAN, status="SUCCESS"))

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

import unittest
from unittest.mock import patch, mock_open

class TestLockAuditExceptions(unittest.TestCase):
    def test_read_lock_audit_jsonl_invalid_json(self):
        invalid_json = '{"valid": "json"}\n{"invalid": "json\n'
        test_path = Path("test.jsonl")

        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=invalid_json)):
                with patch("usa_signal_bot.scheduler.lock_audit.logger.warning") as mock_warning:
                    records = read_lock_audit_jsonl(test_path)

                    self.assertEqual(len(records), 1)
                    self.assertEqual(records[0], {"valid": "json"})
                    mock_warning.assert_called_once()
                    self.assertIn("Failed to parse JSON line", mock_warning.call_args[0][0])

    def test_read_lock_audit_jsonl_file_error(self):
        test_path = Path("test.jsonl")

        with patch("pathlib.Path.exists", return_value=True):
            # Mock open to raise an exception
            mock_open_file = mock_open()
            mock_open_file.side_effect = PermissionError("Permission denied")

            with patch("builtins.open", mock_open_file):
                with patch("usa_signal_bot.scheduler.lock_audit.logger.error") as mock_error:
                    records = read_lock_audit_jsonl(test_path)

                    self.assertEqual(len(records), 0)
                    mock_error.assert_called_once()
                    self.assertIn("Failed to read lock audit file", mock_error.call_args[0][0])
