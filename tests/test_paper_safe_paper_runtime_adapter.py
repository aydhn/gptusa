from usa_signal_bot.paper_safe_dossier.paper_runtime_adapter import (
    build_read_only_paper_snapshot_for_paper_safe_dossier,
    build_pre_paper_runtime_snapshot_for_dossier,
    validate_paper_runtime_not_mutated_by_paper_safe_dossier
)

def test_paper_safe_paper_runtime_adapter():
    payload = {"test": 123, "paper_state_committed": True}
    snapshot = build_read_only_paper_snapshot_for_paper_safe_dossier(payload)

    assert snapshot["test"] == 123
    assert snapshot["is_read_only_snapshot"] is True
    assert snapshot["paper_state_committed"] is False

    pre = build_pre_paper_runtime_snapshot_for_dossier(payload)
    assert pre["is_pre_paper_runtime_snapshot"] is True

    errors = validate_paper_runtime_not_mutated_by_paper_safe_dossier(payload, payload)
    assert len(errors) == 0

    errors = validate_paper_runtime_not_mutated_by_paper_safe_dossier(payload, {"test": 124})
    assert len(errors) > 0
