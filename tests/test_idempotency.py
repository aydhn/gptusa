import tempfile
from pathlib import Path

from usa_signal_bot.scheduler.idempotency import IdempotencyStore, create_idempotency_record, idempotency_records_to_text
from usa_signal_bot.core.enums import RunLockScope, IdempotencyStatus

def test_idempotency_store():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "idemp.jsonl"
        store = IdempotencyStore(p)

        # initial load
        assert len(store.load_records()) == 0

        # append
        store.mark_in_progress("key1", RunLockScope.SCAN, "run1")
        assert len(store.load_records()) == 1

        # find
        r = store.find_by_key("key1")
        assert r is not None
        assert r.status == IdempotencyStatus.IN_PROGRESS

        # mark completed
        store.mark_completed("key1")
        r = store.find_by_key("key1")
        assert r.status == IdempotencyStatus.COMPLETED_BEFORE

        # prune
        pruned = store.prune_expired(max_age_days=-1, dry_run=True)
        assert len(pruned) > 0 # should be pruned
        assert len(store.load_records()) > 0 # but not deleted

        store.prune_expired(max_age_days=-1, dry_run=False)
        assert len(store.load_records()) == 0

def test_idempotency_records_to_text():
    r = create_idempotency_record("k1", RunLockScope.SCAN, "r1", IdempotencyStatus.NEW)
    txt = idempotency_records_to_text([r])
    assert "Idempotency Records" in txt
