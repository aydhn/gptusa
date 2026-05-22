from usa_signal_bot.paper_readiness_confirmation.pre_rehearsal_adapter import (
    confirmation_evidence_from_pre_rehearsal,
    pre_rehearsal_supports_readiness_confirmation
)

def test_confirmation_evidence_from_pre_rehearsal():
    res = confirmation_evidence_from_pre_rehearsal({"review_id": "123"})
    assert res == ["pre_rehearsal_123"]

def test_pre_rehearsal_supports_readiness_confirmation():
    supports, _ = pre_rehearsal_supports_readiness_confirmation({"status": "PASSED"})
    assert supports is True

    supports, reasons = pre_rehearsal_supports_readiness_confirmation({"status": "FAILED"})
    assert supports is False
    assert "did not pass" in reasons[0]
