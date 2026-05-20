import pytest
from usa_signal_bot.paper_quarantine.release_packaging_adapter import (
    bundle_payload_quarantine_refs,
    bundle_supports_quarantine,
    attach_quarantine_metadata_to_bundle_payload,
)

def test_adapter(mocker):
    payload = {"quarantine_candidate_id": "c1", "bundle_id": "b1"}
    refs = bundle_payload_quarantine_refs(payload)
    assert refs["candidate_id"] == "c1"

    sup, _ = bundle_supports_quarantine(payload)
    assert sup is True

    r = mocker.Mock()
    c = mocker.Mock()
    c.candidate_id = "c2"
    c.status.value = "enrolled"
    r.candidates = [c]

    attached = attach_quarantine_metadata_to_bundle_payload({}, r)
    assert attached["quarantine_candidate_id"] == "c2"
