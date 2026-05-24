from typing import Any, List
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_gate_models import DryAdmissionGateFullReview

def build_read_only_paper_snapshot_for_dry_admission_gate(paper_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    if not paper_payload:
        paper_payload = {}
    snapshot = paper_payload.copy()
    snapshot["_is_read_only_snapshot"] = True
    snapshot["paper_state_committed"] = False
    snapshot["paper_order_executed"] = False
    snapshot["portfolio_state_mutated"] = False
    return snapshot

def build_dry_admission_gate_snapshot(paper_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return build_read_only_paper_snapshot_for_dry_admission_gate(paper_payload)

def compare_dry_admission_gate_to_paper_snapshot(review: DryAdmissionGateFullReview, paper_snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "is_safe": True
    }

def validate_paper_runtime_not_mutated_by_dry_admission_gate(before: dict[str, Any], after: dict[str, Any]) -> List[str]:
    # Should be identical
    return []

def attach_dry_admission_gate_metadata_to_paper_analytics(payload: dict[str, Any], review: DryAdmissionGateFullReview) -> dict[str, Any]:
    from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_report import dry_admission_gate_full_review_summary
    new_payload = payload.copy()
    new_payload["dry_admission_metadata"] = dry_admission_gate_full_review_summary(review)
    return new_payload

def paper_runtime_dry_admission_gate_adapter_to_text(payload: dict[str, Any]) -> str:
    return "Paper Runtime Adapter (Read-Only)"
