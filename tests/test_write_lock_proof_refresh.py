from usa_signal_bot.paper_dry_admission.write_lock_proof_refresh import refresh_runtime_write_lock_proof
from usa_signal_bot.core.enums import WriteLockProofRefreshStatus

def test_write_lock_proof_refresh():
    refresh = refresh_runtime_write_lock_proof(
        paper_payload_before={"hash": "abc"},
        paper_payload_after={"hash": "abc"}
    )
    assert refresh.hash_unchanged
    assert refresh.status == WriteLockProofRefreshStatus.REFRESHED
    assert refresh.all_writes_blocked
    assert refresh.unblocked_write_attempt_count == 0

    refresh_bad = refresh_runtime_write_lock_proof(
        paper_payload_before={"hash": "abc"},
        paper_payload_after={"hash": "def"}
    )
    assert not refresh_bad.hash_unchanged
    assert refresh_bad.status == WriteLockProofRefreshStatus.FAILED
