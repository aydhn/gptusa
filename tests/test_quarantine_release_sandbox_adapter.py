import pytest
from usa_signal_bot.paper_quarantine.release_sandbox_adapter import (
    sandbox_payload_quarantine_refs,
    sandbox_supports_quarantine,
    attach_quarantine_metadata_to_sandbox_payload,
)

def test_adapter(mocker):
    payload = {"quarantine_candidate_id": "c1", "sandbox_run_id": "s1"}
    refs = sandbox_payload_quarantine_refs(payload)
    assert refs["candidate_id"] == "c1"

    sup, _ = sandbox_supports_quarantine(payload)
    assert sup is True

    r = mocker.Mock()
    c = mocker.Mock()
    c.candidate_id = "c2"
    r.candidates = [c]
    r.tickets = []
    r.bridge_plans = []

    attached = attach_quarantine_metadata_to_sandbox_payload({}, r)
    assert attached["quarantine_candidate_id"] == "c2"
