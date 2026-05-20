import pytest
from usa_signal_bot.paper_quarantine.paper_shadow_governance_adapter import (
    candidate_from_shadow_governance_review,
    ticket_from_shadow_governance_review,
    bridge_plan_from_shadow_governance_review,
    quarantine_review_from_shadow_governance_review,
    attach_quarantine_to_shadow_governance_payload,
)

def test_adapter():
    payload = {"decision": "ACCEPT_AS_SANDBOXED_PAPER_CANDIDATE", "score": 80.0}
    c = candidate_from_shadow_governance_review(payload)
    assert c.status.value == "enrolled"

    t = ticket_from_shadow_governance_review(payload)
    assert t.read_only is True

    p = bridge_plan_from_shadow_governance_review(payload)
    assert p.paper_state_mutation_enabled is False

    r = quarantine_review_from_shadow_governance_review(payload)
    assert r.candidates[0].status.value == 'enrolled'

    attached = attach_quarantine_to_shadow_governance_payload({}, r)
    assert attached["quarantine_status"] == "enrolled"
