from usa_signal_bot.paper_safe_dossier.boundary_adapter import (
    paper_safe_dossier_evidence_from_boundary,
    boundary_supports_paper_safe_dossier,
    attach_paper_safe_dossier_hint_to_boundary_payload,
    boundary_paper_safe_dossier_summary,
    boundary_adapter_to_text
)
from usa_signal_bot.paper_safe_dossier.no_order_adapter import (
    paper_safe_dossier_evidence_from_no_order,
    no_order_supports_paper_safe_dossier,
    attach_paper_safe_dossier_hint_to_no_order_payload,
    no_order_paper_safe_dossier_summary,
    no_order_adapter_to_text
)
from usa_signal_bot.paper_safe_dossier.paper_safe_adapter import (
    paper_safe_dossier_from_paper_safe_gate,
    non_execution_seal_from_paper_safe_gate,
    runtime_map_from_paper_safe_gate,
    paper_safe_dossier_full_review_from_paper_safe_gate,
    attach_paper_safe_dossier_metadata_to_paper_safe_payload,
    paper_safe_gate_dossier_summary,
    paper_safe_adapter_to_text
)
from usa_signal_bot.paper_safe_dossier.dossier_report import build_paper_safe_dossier_full_review

def test_paper_safe_adapters():
    ps_payload = {"gates": [{"gate_id": "g1", "candidate_id": "c1", "decision": "VALIDATED_PAPER_SAFE"}]}
    review = build_paper_safe_dossier_full_review(ps_payload)

    # Boundary
    b_payload = {"report_type": "BOUNDARY_CERTIFICATE_REPORT", "review_id": "rev1"}
    assert paper_safe_dossier_evidence_from_boundary(b_payload) == ["rev1"]
    supports, _ = boundary_supports_paper_safe_dossier(b_payload)
    assert supports
    res = attach_paper_safe_dossier_hint_to_boundary_payload(b_payload, review)
    assert res["paper_safe_dossier_hint"] == review.review_id
    assert boundary_paper_safe_dossier_summary(res)["hint"] == review.review_id
    assert boundary_adapter_to_text(res) != ""

    # No Order
    n_payload = {"report_type": "NO_ORDER_DOSSIER_REPORT", "review_id": "rev2"}
    assert paper_safe_dossier_evidence_from_no_order(n_payload) == ["rev2"]
    supports, _ = no_order_supports_paper_safe_dossier(n_payload)
    assert supports
    res = attach_paper_safe_dossier_hint_to_no_order_payload(n_payload, review)
    assert res["paper_safe_dossier_hint"] == review.review_id
    assert no_order_paper_safe_dossier_summary(res)["hint"] == review.review_id
    assert no_order_adapter_to_text(res) != ""

    # Paper Safe
    dossier = paper_safe_dossier_from_paper_safe_gate(ps_payload)
    assert dossier is not None
    seal = non_execution_seal_from_paper_safe_gate(ps_payload)
    assert seal is not None
    rmap = runtime_map_from_paper_safe_gate(ps_payload)
    assert rmap is not None
    full = paper_safe_dossier_full_review_from_paper_safe_gate(ps_payload)
    assert full is not None
    res = attach_paper_safe_dossier_metadata_to_paper_safe_payload(ps_payload, review)
    assert res["paper_safe_dossier_review_id"] == review.review_id
    assert paper_safe_gate_dossier_summary(res)["review_id"] == review.review_id
    assert paper_safe_adapter_to_text(res) != ""
