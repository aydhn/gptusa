from usa_signal_bot.paper_readiness_confirmation.firewall_audit_ingestion import (
    ingest_firewall_audit_review,
    firewall_audit_supports_readiness_confirmation
)

def test_ingest_firewall_audit_review():
    res = ingest_firewall_audit_review({"status": "test"})
    assert res["status"] == "test"

def test_firewall_audit_supports_readiness_confirmation():
    payload = {
        "decision": "CONTINUE_WITH_ACTIVATION_DENIED_AUDIT",
        "activation_allowed": False,
        "zero_mutation_audit": {"status": "PASSED"}
    }
    supports, reasons = firewall_audit_supports_readiness_confirmation(payload)
    assert supports is True
    assert len(reasons) == 0

def test_firewall_audit_supports_readiness_confirmation_fail():
    payload = {
        "decision": "CONTINUE_WITH_ACTIVATION_DENIED_AUDIT",
        "activation_allowed": True,
        "zero_mutation_audit": {"status": "PASSED"}
    }
    supports, reasons = firewall_audit_supports_readiness_confirmation(payload)
    assert supports is False
    assert "activation_allowed must be false" in reasons
