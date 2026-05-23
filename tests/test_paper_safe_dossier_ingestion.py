from usa_signal_bot.paper_safe_dossier.paper_safe_ingestion import (
    ingest_paper_safe_gate_full_review,
    extract_final_paper_safe_gate,
    extract_boundary_replay_result,
    extract_frozen_evidence_integrity_audit,
    extract_paper_safe_rules,
    extract_paper_safe_assertions,
    extract_paper_safe_candidate_id,
    extract_paper_safe_decision,
    paper_safe_gate_supports_dossier
)
from usa_signal_bot.core.enums import PaperSafeGateReportType

def test_paper_safe_ingestion():
    payload = {
        "report_type": PaperSafeGateReportType.FINAL_PAPER_SAFE_GATE_REPORT.value,
        "review_id": "rev1",
        "gates": [{"gate_id": "g1", "candidate_id": "c1", "decision": "VALIDATED_PAPER_SAFE"}],
        "replay_results": [{"replay_result_id": "r1"}],
        "integrity_audits": [{"audit_id": "a1", "tamper_count": 0}],
        "rules": [],
        "assertions": []
    }

    assert ingest_paper_safe_gate_full_review(payload) == payload
    assert extract_final_paper_safe_gate(payload)["gate_id"] == "g1"
    assert extract_boundary_replay_result(payload)["replay_result_id"] == "r1"
    assert extract_frozen_evidence_integrity_audit(payload)["audit_id"] == "a1"
    assert extract_paper_safe_rules(payload) == []
    assert extract_paper_safe_assertions(payload) == []
    assert extract_paper_safe_candidate_id(payload) == "c1"
    assert extract_paper_safe_decision(payload) == "VALIDATED_PAPER_SAFE"

    supports, reasons = paper_safe_gate_supports_dossier(payload)
    assert supports is True
    assert reasons == []

    # Tamper test
    payload["integrity_audits"][0]["tamper_count"] = 1
    supports, reasons = paper_safe_gate_supports_dossier(payload)
    assert supports is False
    assert "Frozen evidence tamper detected." in reasons
