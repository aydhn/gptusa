import pytest
from usa_signal_bot.paper_quarantine.paper_runtime_adapter import (
    build_read_only_paper_snapshot_for_quarantine,
    compare_quarantine_candidate_to_paper_snapshot,
    validate_paper_payload_not_mutated,
    attach_quarantine_metadata_to_paper_analytics,
)

def test_adapter(mocker):
    s = build_read_only_paper_snapshot_for_quarantine({"data": 1})
    assert s.read_only is True

    c = mocker.Mock()
    c.candidate_id = "c1"
    comp = compare_quarantine_candidate_to_paper_snapshot(c, s)
    assert comp["candidate_id"] == "c1"

    errs = validate_paper_payload_not_mutated({"timestamp": 1}, {"timestamp": 2})
    assert len(errs) > 0

    errs = validate_paper_payload_not_mutated({}, {"paper_state_committed": True})
    assert len(errs) > 0

    r = mocker.Mock()
    r.candidates = [c]
    attached = attach_quarantine_metadata_to_paper_analytics({}, r)
    assert attached["paper_state_committed"] is False
