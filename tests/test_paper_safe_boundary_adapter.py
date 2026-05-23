from usa_signal_bot.paper_safe_dossier.boundary_adapter import (
    paper_safe_dossier_evidence_from_boundary,
    boundary_supports_paper_safe_dossier,
    attach_paper_safe_dossier_hint_to_boundary_payload,
    boundary_paper_safe_dossier_summary,
    boundary_adapter_to_text
)
from usa_signal_bot.paper_safe_dossier.dossier_report import build_paper_safe_dossier_full_review

def test_paper_safe_boundary_adapter():
    payload = {"report_type": "BOUNDARY_CERTIFICATE_REPORT", "review_id": "rev1"}

    assert paper_safe_dossier_evidence_from_boundary(payload) == ["rev1"]

    supports, reasons = boundary_supports_paper_safe_dossier(payload)
    assert supports is True

    payload["report_type"] = "OTHER"
    supports, reasons = boundary_supports_paper_safe_dossier(payload)
    assert supports is False

    ps_payload = {"gates": [{"gate_id": "g1", "candidate_id": "c1", "decision": "VALIDATED_PAPER_SAFE"}]}
    review = build_paper_safe_dossier_full_review(ps_payload)

    payload = attach_paper_safe_dossier_hint_to_boundary_payload(payload, review)
    assert payload["paper_safe_dossier_hint"] == review.review_id

    summary = boundary_paper_safe_dossier_summary(payload)
    assert summary["hint"] == review.review_id

    text = boundary_adapter_to_text(payload)
    assert review.review_id in text
