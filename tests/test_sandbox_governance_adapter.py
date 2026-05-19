import pytest
from usa_signal_bot.release_sandbox.sandbox_models import ReleaseSandboxReview
from usa_signal_bot.release_sandbox.governance_adapter import (
    sandbox_governance_checklist_from_review,
    governance_bundle_sandbox_allowed,
    attach_sandbox_review_to_governance_payload,
    governance_adapter_to_text
)

def test_governance_adapter():
    payload = {"sandbox_activation_status": "VALIDATED"}

    cl = sandbox_governance_checklist_from_review(payload)
    assert len(cl) == 2
    assert cl[0]["status"] == "PASS"

    payload["sandbox_activation_status"] = "BLOCKED"
    allowed, warns = governance_bundle_sandbox_allowed(payload)
    assert allowed is False
    assert len(warns) == 1

    review = ReleaseSandboxReview("rev1", "now", "FULL_SANDBOX_REVIEW", [], [], [], [], {}, [], [])
    payload = attach_sandbox_review_to_governance_payload(payload, review)
    assert payload["sandbox_review_id"] == "rev1"

    txt = governance_adapter_to_text(payload)
    assert "Sandbox Status" in txt
