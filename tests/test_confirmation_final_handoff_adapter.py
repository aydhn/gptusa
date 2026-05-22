from usa_signal_bot.paper_readiness_confirmation.final_handoff_adapter import (
    confirmation_evidence_from_final_handoff,
    final_handoff_supports_readiness_confirmation
)

def test_confirmation_evidence_from_final_handoff():
    res = confirmation_evidence_from_final_handoff({"review_id": "123"})
    assert res == ["final_handoff_123"]

def test_final_handoff_supports_readiness_confirmation():
    supports, _ = final_handoff_supports_readiness_confirmation({"decision": "APPROVE_FOR_ACTIVATION_DENIED_AUDIT"})
    assert supports is True

    supports, reasons = final_handoff_supports_readiness_confirmation({"decision": "REJECT"})
    assert supports is False
    assert "did not approve" in reasons[0]
