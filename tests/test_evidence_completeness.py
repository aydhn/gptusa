from usa_signal_bot.paper_readiness_confirmation.evidence_completeness import evaluate_confirmation_evidence_completeness

def test_evaluate_confirmation_evidence_completeness_missing():
    comp = evaluate_confirmation_evidence_completeness({})
    assert comp["is_complete"] is False
    assert "firewall_audit_review" in comp["missing"]

def test_evaluate_confirmation_evidence_completeness_complete():
    payload = {
        "zero_mutation_audit": {"status": "PASSED"},
        "firewall_replay_result": {"status": "PASSED"},
        "pre_paper_evidence_refresh": {"status": "FRESH"}
    }
    comp = evaluate_confirmation_evidence_completeness(payload)
    assert comp["is_complete"] is True
    assert len(comp["missing"]) == 0
    assert len(comp["stale"]) == 0
