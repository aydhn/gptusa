import pytest
from usa_signal_bot.paper_quarantine.paper_snapshot_ref import (
    stable_snapshot_hash,
    redact_snapshot_sensitive_fields,
    build_read_only_paper_snapshot_ref,
    paper_snapshot_ref_to_text,
)

def test_stable_hash():
    h1 = stable_snapshot_hash({"a": 1, "b": 2})
    h2 = stable_snapshot_hash({"b": 2, "a": 1})
    assert h1 == h2

def test_redact():
    r = redact_snapshot_sensitive_fields({"api_key": "secret", "other": 1})
    assert r["api_key"] == "[REDACTED]"
    assert r["other"] == 1

def test_build():
    ref = build_read_only_paper_snapshot_ref({"api_key": "secret", "data": 123})
    assert ref.read_only is True
    assert ref.allows_mutation is False
    assert ref.snapshot_hash is not None

def test_to_text():
    ref = build_read_only_paper_snapshot_ref()
    assert "Read Only: True" in paper_snapshot_ref_to_text(ref)
