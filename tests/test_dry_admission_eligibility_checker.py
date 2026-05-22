from usa_signal_bot.paper_dry_admission.eligibility_checker import (
    evaluate_dry_admission_eligibility,
    dry_admission_safety_flags_from_no_write
)
from usa_signal_bot.core.enums import PaperModeDryAdmissionDecision, DryAdmissionRiskFlag

def test_eligibility_checker():
    payload = {
        "contracts": [{"contract_id": "c1", "activation_denied": True, "activation_allowed": False}],
        "replays": [{"replay_id": "r1"}],
        "preflights": [{"preflight_id": "p1", "decision": "PASS_NO_WRITE_PREFLIGHT", "mutation_detected": False, "all_writes_blocked": True, "activation_allowed": False}]
    }
    decision = evaluate_dry_admission_eligibility(payload)
    assert decision == PaperModeDryAdmissionDecision.RUN_DRY_ADMISSION_REHEARSAL

    flags = dry_admission_safety_flags_from_no_write(payload)
    assert len(flags) == 0

    payload_bad = {
        "contracts": [{"contract_id": "c1", "activation_denied": False, "activation_allowed": True}],
        "replays": [{"replay_id": "r1"}],
        "preflights": [{"preflight_id": "p1", "decision": "PASS_NO_WRITE_PREFLIGHT", "mutation_detected": True, "all_writes_blocked": False, "activation_allowed": True}]
    }
    flags_bad = dry_admission_safety_flags_from_no_write(payload_bad)
    assert DryAdmissionRiskFlag.NO_WRITE_CONTRACT_INVALID in flags_bad
    assert DryAdmissionRiskFlag.ACTIVATION_ALLOWED_RISK in flags_bad
    assert DryAdmissionRiskFlag.PAPER_STATE_MUTATION_RISK in flags_bad
    assert DryAdmissionRiskFlag.DRY_ADMISSION_WRITE_ATTEMPT in flags_bad
    assert DryAdmissionRiskFlag.ACTIVE_PAPER_ENABLE_RISK in flags_bad
