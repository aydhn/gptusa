from usa_signal_bot.paper_dry_admission.write_lock_proof_refresh import refresh_runtime_write_lock_proof
from usa_signal_bot.paper_dry_admission.write_lock_refresh_validator import validate_write_lock_refresh_safety

def test_write_lock_refresh_validator():
    refresh = refresh_runtime_write_lock_proof(
        paper_payload_before={"hash": "abc"},
        paper_payload_after={"hash": "abc"}
    )
    issues = validate_write_lock_refresh_safety(refresh)
    assert len(issues) == 0

    refresh_bad = refresh_runtime_write_lock_proof(
        paper_payload_before={"hash": "abc"},
        paper_payload_after={"hash": "def"}
    )
    issues_bad = validate_write_lock_refresh_safety(refresh_bad)
    assert len(issues_bad) > 0
