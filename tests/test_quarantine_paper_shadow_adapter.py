import pytest
from usa_signal_bot.paper_quarantine.paper_shadow_adapter import (
    quarantine_evidence_from_shadow_rehearsal,
    shadow_rehearsal_supports_quarantine,
    attach_quarantine_hint_to_shadow_rehearsal,
)

def test_adapter(mocker):
    payload = {"rehearsal_id": "r1"}
    ev = quarantine_evidence_from_shadow_rehearsal(payload)
    assert ev["rehearsal_id"] == "r1"

    sup, _ = shadow_rehearsal_supports_quarantine(payload)
    assert sup is True

    c = mocker.Mock()
    c.candidate_id = "c1"
    c.status.value = "enrolled"
    attached = attach_quarantine_hint_to_shadow_rehearsal({}, c)
    assert attached["quarantine_candidate_id"] == "c1"
