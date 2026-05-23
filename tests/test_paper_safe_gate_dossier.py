from usa_signal_bot.paper_safe_dossier.paper_safe_gate_dossier import build_paper_safe_gate_dossier
from usa_signal_bot.core.enums import PaperSafeDossierStatus

def test_paper_safe_gate_dossier():
    payload = {
        "review_id": "r1",
        "gates": [{"gate_id": "g1", "candidate_id": "c1", "decision": "VALIDATED_PAPER_SAFE"}],
        "replay_results": [{"replay_result_id": "rr1"}],
        "integrity_audits": [{"audit_id": "a1", "tamper_count": 0}],
        "rules": [{"rule_id": "ru1"}],
        "assertions": [{"assertion_id": "as1"}]
    }

    dossier = build_paper_safe_gate_dossier(payload)
    assert dossier.status == PaperSafeDossierStatus.CREATED
    assert dossier.candidate_id == "c1"
    assert dossier.sealed is True
    assert dossier.immutable is True
    assert dossier.manual_review_required is True
    assert dossier.activation_denied is True
    assert dossier.activation_allowed is False
    assert dossier.paper_safe_gate_passed is True
    assert dossier.all_writes_blocked is True
