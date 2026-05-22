from usa_signal_bot.paper_dry_admission.dry_admission_report import build_dry_admission_full_review

def test_dry_admission_report():
    payload = {
        "contracts": [{"contract_id": "c1", "activation_denied": True, "activation_allowed": False}],
        "replays": [{"replay_id": "r1"}],
        "preflights": [{"preflight_id": "p1", "decision": "PASS_NO_WRITE_PREFLIGHT", "mutation_detected": False, "all_writes_blocked": True, "activation_allowed": False}]
    }
    review = build_dry_admission_full_review(payload)
    assert len(review.plans) == 1
    assert len(review.runs) == 1
