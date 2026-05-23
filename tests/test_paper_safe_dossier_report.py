from usa_signal_bot.paper_safe_dossier.dossier_report import build_paper_safe_dossier_full_review, paper_safe_dossier_full_review_summary
from usa_signal_bot.core.enums import PaperSafeDossierReportType

def test_paper_safe_dossier_report():
    payload = {"gates": [{"gate_id": "g1", "candidate_id": "c1", "decision": "VALIDATED_PAPER_SAFE"}], "integrity_audits": [{"tamper_count": 0}]}
    review = build_paper_safe_dossier_full_review(payload)

    assert review.report_type == PaperSafeDossierReportType.FULL_PAPER_SAFE_DOSSIER_REVIEW
    assert len(review.dossiers) == 1
    assert len(review.non_execution_seals) == 1
    assert len(review.runtime_maps) == 1
    assert len(review.audit_entries) == 3

    summary = paper_safe_dossier_full_review_summary(review)
    assert summary["dossiers"] == 1
    assert summary["seals"] == 1
