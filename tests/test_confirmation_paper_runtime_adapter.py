from usa_signal_bot.paper_readiness_confirmation.paper_runtime_adapter import (
    build_read_only_paper_snapshot_for_readiness_confirmation,
    validate_paper_runtime_not_mutated_by_readiness_confirmation
)

def test_build_read_only_paper_snapshot_for_readiness_confirmation():
    payload = {"state": "test"}
    res = build_read_only_paper_snapshot_for_readiness_confirmation(payload)
    assert res["state"] == "test"
    assert res["is_read_only_snapshot"] is True
    assert "is_read_only_snapshot" not in payload

def test_validate_paper_runtime_not_mutated_by_readiness_confirmation():
    before = {"state": "test"}
    after = {"state": "test"}
    errors = validate_paper_runtime_not_mutated_by_readiness_confirmation(before, after)
    assert len(errors) == 0

    after = {"state": "changed"}
    errors = validate_paper_runtime_not_mutated_by_readiness_confirmation(before, after)
    assert len(errors) == 1
    assert "mutated" in errors[0]
