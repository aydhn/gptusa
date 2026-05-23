from usa_signal_bot.paper_safe_dossier.dossier_continuity import validate_paper_safe_dossier_continuity
from usa_signal_bot.paper_safe_dossier.paper_safe_gate_dossier import build_paper_safe_gate_dossier
from usa_signal_bot.paper_safe_dossier.non_execution_acceptance_seal import build_non_execution_acceptance_seal
from usa_signal_bot.paper_safe_dossier.local_runtime_map import build_pre_paper_local_runtime_map

def test_paper_safe_dossier_continuity():
    payload = {"gates": [{"gate_id": "g1", "candidate_id": "c1", "decision": "VALIDATED_PAPER_SAFE"}], "integrity_audits": [{"tamper_count": 0}]}
    dossier = build_paper_safe_gate_dossier(payload)
    seal = build_non_execution_acceptance_seal(payload)
    rmap = build_pre_paper_local_runtime_map(payload)

    errors = validate_paper_safe_dossier_continuity(dossier=dossier, seal=seal, runtime_map=rmap)
    assert len(errors) == 0

    dossier.activation_denied = False
    errors = validate_paper_safe_dossier_continuity(dossier=dossier, seal=seal, runtime_map=rmap)
    assert "Dossier activation is not denied." in errors
