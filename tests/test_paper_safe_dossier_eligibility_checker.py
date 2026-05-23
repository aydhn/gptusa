from usa_signal_bot.paper_safe_dossier.eligibility_checker import (
    evaluate_paper_safe_dossier_eligibility,
    paper_safe_dossier_safety_flags_from_payload
)
from usa_signal_bot.core.enums import PaperSafeDossierDecision, PaperSafeGateReportType

def test_paper_safe_dossier_eligibility():
    payload = {
        "report_type": PaperSafeGateReportType.FINAL_PAPER_SAFE_GATE_REPORT.value,
        "gates": [{"gate_id": "g1", "decision": "VALIDATED_PAPER_SAFE"}],
        "integrity_audits": [{"tamper_count": 0}]
    }
    decision = evaluate_paper_safe_dossier_eligibility(payload)
    assert decision == PaperSafeDossierDecision.CREATE_PAPER_SAFE_DOSSIER

    payload["gates"][0]["decision"] = "REJECT"
    decision = evaluate_paper_safe_dossier_eligibility(payload)
    assert decision == PaperSafeDossierDecision.REJECT

    payload["gates"][0]["decision"] = "UNKNOWN"
    decision = evaluate_paper_safe_dossier_eligibility(payload)
    assert decision == PaperSafeDossierDecision.INCONCLUSIVE

    payload["gates"] = []
    decision = evaluate_paper_safe_dossier_eligibility(payload)
    assert decision == PaperSafeDossierDecision.REQUEST_PAPER_SAFE_GATE_REFRESH

    payload["gates"] = [{"gate_id": "g1", "decision": "VALIDATED_PAPER_SAFE", "activation_allowed": True}]
    payload["integrity_audits"][0]["tamper_count"] = 1
    flags = paper_safe_dossier_safety_flags_from_payload(payload)
    assert len(flags) == 2
