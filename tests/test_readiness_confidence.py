from usa_signal_bot.paper_readiness_confirmation.readiness_confidence import calculate_readiness_confidence
from usa_signal_bot.core.enums import ReadinessConfidenceLevel

def test_calculate_readiness_confidence_insufficient():
    level = calculate_readiness_confidence({})
    assert level == ReadinessConfidenceLevel.INSUFFICIENT_DATA

def test_calculate_readiness_confidence_high():
    payload = {
        "decision": "CONTINUE_WITH_ACTIVATION_DENIED_AUDIT",
        "activation_allowed": False,
        "zero_mutation_audit": {"status": "PASSED"},
        "firewall_replay_result": {"status": "PASSED"},
        "pre_paper_evidence_refresh": {"status": "FRESH"}
    }
    level = calculate_readiness_confidence(payload)
    assert level == ReadinessConfidenceLevel.HIGH

def test_calculate_readiness_confidence_medium():
    payload = {
        "decision": "CONTINUE_WITH_ACTIVATION_DENIED_AUDIT",
        "activation_allowed": False,
        "zero_mutation_audit": {"status": "PASSED"},
        "firewall_replay_result": {"status": "PASSED"},
        "pre_paper_evidence_refresh": {"status": "STALE"}
    }
    level = calculate_readiness_confidence(payload)
    assert level == ReadinessConfidenceLevel.MEDIUM

def test_calculate_readiness_confidence_blocked():
    payload = {
        "decision": "CONTINUE_WITH_ACTIVATION_DENIED_AUDIT",
        "activation_allowed": True,
        "zero_mutation_audit": {"status": "PASSED"}
    }
    level = calculate_readiness_confidence(payload)
    assert level == ReadinessConfidenceLevel.BLOCKED
