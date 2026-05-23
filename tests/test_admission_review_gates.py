from usa_signal_bot.paper_admission_review.admission_gates import default_admission_review_gates
from usa_signal_bot.core.enums import AdmissionReviewGateStatus

def test_default_admission_review_gates():
    payload = {
        "dry_admission_run": {"status": "COMPLETED_NO_WRITE"},
        "write_lock_refresh": {"status": "VALIDATED"},
        "human_approval_ledger": {"acknowledged_not_activation": True},
        "activation_denied": True,
        "activation_allowed": False,
        "all_writes_blocked": True,
        "mutation_detected": False,
        "allows_broker_execution": False,
        "allows_telegram_real_send": False,
        "allows_config_patch": False
    }
    gates = default_admission_review_gates(payload)
    assert len(gates) == 11
    assert all(g.status == AdmissionReviewGateStatus.PASS for g in gates)
