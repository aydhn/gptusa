from usa_signal_bot.paper_admission_review.admission_report import build_admission_review_full_report, admission_review_limitations_text

def test_build_admission_review_full_report():
    payload = {
        "activation_denied": True,
        "activation_allowed": False,
        "all_writes_blocked": True,
        "mutation_detected": False,
        "dry_admission_run": {"status": "COMPLETED_NO_WRITE"},
        "write_lock_refresh": {"status": "VALIDATED"},
        "human_approval_ledger": {
            "completed_scopes": {
                "NO_WRITE_REVIEW_ACKNOWLEDGEMENT": True,
                "SAFETY_REVIEW_ACKNOWLEDGEMENT": True,
                "EVIDENCE_REVIEW_ACKNOWLEDGEMENT": True,
                "NOT_ACTIVATION_APPROVAL": True
            },
            "acknowledged_no_write": True,
            "acknowledged_not_activation": True,
            "activation_allowed": False
        },
        "evidence_refs": ["ref1"]
    }
    report = build_admission_review_full_report(payload)
    assert len(report.admission_reviews) == 1
    assert len(report.ledger_reconciliations) == 1
    assert len(report.evidence_seals) == 1
    assert len(report.transition_checkpoints) == 1
    assert "LIMITATIONS" in admission_review_limitations_text()
