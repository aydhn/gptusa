from usa_signal_bot.paper_safe_dossier.dossier_audit import audit_entry_from_paper_safe_dossier, audit_entry_from_non_execution_seal, audit_entry_from_runtime_map
from usa_signal_bot.paper_safe_dossier.paper_safe_gate_dossier import build_paper_safe_gate_dossier
from usa_signal_bot.paper_safe_dossier.non_execution_acceptance_seal import build_non_execution_acceptance_seal
from usa_signal_bot.paper_safe_dossier.local_runtime_map import build_pre_paper_local_runtime_map

def test_paper_safe_dossier_audit():
    payload = {"gates": [{"gate_id": "g1", "candidate_id": "c1", "decision": "VALIDATED_PAPER_SAFE"}]}

    dossier = build_paper_safe_gate_dossier(payload)
    seal = build_non_execution_acceptance_seal(payload)
    rmap = build_pre_paper_local_runtime_map(payload)

    e1 = audit_entry_from_paper_safe_dossier(dossier)
    assert e1.entity_type == "PaperSafeGateDossier"
    assert e1.action == "CREATE_DOSSIER"

    e2 = audit_entry_from_non_execution_seal(seal)
    assert e2.entity_type == "NonExecutionAcceptanceSeal"
    assert e2.action == "CREATE_SEAL"

    e3 = audit_entry_from_runtime_map(rmap)
    assert e3.entity_type == "PrePaperLocalRuntimeMap"
    assert e3.action == "CREATE_RUNTIME_MAP"
