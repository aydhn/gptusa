from usa_signal_bot.paper_admission_review.dry_admission_evidence import evaluate_admission_evidence_completeness

def test_evaluate_admission_evidence_completeness():
    payload = {
        "evidence": {
            "dry_admission_full_review": {},
            "dry_admission_run": {},
            "no_write_contract": {},
            "write_lock_refresh": {},
            "human_approval_ledger": {},
            "activation_replay_result": {},
            "no_write_continuity_report": {},
            "runtime_write_lock_assertion": {},
            "validation_reports": {},
            "audit_trails": {}
        }
    }
    result = evaluate_admission_evidence_completeness(payload)
    assert result["complete"]

    incomplete = {"evidence": {}}
    result = evaluate_admission_evidence_completeness(incomplete)
    assert not result["complete"]
