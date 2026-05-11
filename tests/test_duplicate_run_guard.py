from usa_signal_bot.scheduler.duplicate_run_guard import (
    build_run_payload_checksum, build_idempotency_key, check_duplicate_run, duplicate_run_check_result_to_text
)
from usa_signal_bot.scheduler.idempotency import create_idempotency_record
from usa_signal_bot.core.enums import RunLockScope, IdempotencyStatus

def test_payload_checksum_deterministic():
    p1 = {"a": 1, "b": 2, "run_id": "r1"}
    p2 = {"a": 1, "b": 2, "run_id": "r2"}
    assert build_run_payload_checksum(p1) == build_run_payload_checksum(p2)

def test_idempotency_key():
    p1 = {"a": 1}
    key = build_idempotency_key(RunLockScope.SCAN, p1)
    assert key.startswith("scan_")

def test_check_duplicate_run_false():
    p1 = {"a": 1}
    res = check_duplicate_run([], RunLockScope.SCAN, p1)
    assert res.duplicate is False
    assert res.status == IdempotencyStatus.NEW

def test_check_duplicate_run_true():
    p1 = {"a": 1}
    key = build_idempotency_key(RunLockScope.SCAN, p1)
    r = create_idempotency_record(key, RunLockScope.SCAN, "r1", IdempotencyStatus.COMPLETED_BEFORE)

    res = check_duplicate_run([r], RunLockScope.SCAN, p1)
    assert res.duplicate is True
    assert res.status == IdempotencyStatus.DUPLICATE

def test_duplicate_text():
    p1 = {"a": 1}
    res = check_duplicate_run([], RunLockScope.SCAN, p1)
    txt = duplicate_run_check_result_to_text(res)
    assert "DuplicateCheck" in txt
