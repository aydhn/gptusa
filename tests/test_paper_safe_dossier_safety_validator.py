from usa_signal_bot.paper_safe_dossier.dossier_safety_validator import validate_paper_safe_dossier_safety
from usa_signal_bot.paper_safe_dossier.paper_safe_gate_dossier import build_paper_safe_gate_dossier
from usa_signal_bot.paper_safe_dossier.non_execution_acceptance_seal import build_non_execution_acceptance_seal

def test_paper_safe_dossier_safety_validator():
    payload = {"gates": [{"gate_id": "g1", "candidate_id": "c1", "decision": "VALIDATED_PAPER_SAFE"}]}
    dossier = build_paper_safe_gate_dossier(payload)
    seal = build_non_execution_acceptance_seal(payload)

    errors = validate_paper_safe_dossier_safety(dossier=dossier, seal=seal)
    assert len(errors) == 0

    dossier.safety_flags.append(None) # just add something that is not blocking
    errors = validate_paper_safe_dossier_safety(dossier=dossier, seal=seal)
    assert len(errors) == 0

    dossier.activation_allowed = True
    errors = validate_paper_safe_dossier_safety(dossier=dossier, seal=seal)
    assert len(errors) > 0
