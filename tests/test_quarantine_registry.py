import pytest
from usa_signal_bot.paper_quarantine.quarantine_models import QuarantinedPaperCandidate
from usa_signal_bot.paper_quarantine.quarantine_registry import (
    register_quarantined_candidate,
    find_quarantined_candidate_by_id,
    find_candidates_by_bundle_id,
    latest_candidate_for_bundle,
)

def test_registry(mocker):
    c = mocker.Mock(spec=QuarantinedPaperCandidate)
    c.candidate_id = "c1"
    c.source_bundle_id = "b1"
    c.created_at_utc = "2024-01-01T00:00:00Z"

    reg = register_quarantined_candidate(c)
    assert len(reg) == 1
    assert find_quarantined_candidate_by_id(reg, "c1").candidate_id == c.candidate_id
    assert len(find_candidates_by_bundle_id(reg, "b1")) == 1
    assert latest_candidate_for_bundle(reg, "b1").candidate_id == c.candidate_id
