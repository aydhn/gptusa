import pytest
import json
from pathlib import Path
from usa_signal_bot.core.enums import ResourceProfileScope
from usa_signal_bot.profiling.profiling_audit import create_profiling_audit_event, write_profiling_audit_jsonl, read_profiling_audit_jsonl

def test_profiling_audit_creation_and_redaction():
    event = create_profiling_audit_event("TEST", "SUCCESS", "msg", metadata={"api_key": "123"})
    assert event.metadata["api_key"] == "***REDACTED***"

def test_profiling_audit_io(tmp_path):
    event = create_profiling_audit_event("TEST", "SUCCESS", "msg", scope=ResourceProfileScope.SCAN)
    path = tmp_path / "audit.jsonl"

    write_profiling_audit_jsonl(path, [event])
    records = read_profiling_audit_jsonl(path)

    assert len(records) == 1
    assert records[0]["event_type"] == "TEST"
    assert records[0]["scope"] == "SCAN"
