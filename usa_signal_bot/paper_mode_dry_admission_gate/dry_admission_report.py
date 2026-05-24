from datetime import datetime, timezone
from typing import Any, List
from usa_signal_bot.core.enums import DryAdmissionGateReportType
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_gate_models import (
    DryAdmissionGateFullReview,
    FinalPaperModeDryAdmissionGate,
    ShadowLaunchReplayResult,
    BoardEvidenceFreezeBundle,
    create_dry_admission_full_review_id
)

def dry_admission_gate_limitations_text() -> str:
    return """
DRY ADMISSION GATE LIMITATIONS:
- No broker/live/demo order.
- No active paper enable.
- No paper admission.
- No shadow launch.
- No paper-mode launch.
- No real paper mutation.
- No paper order.
- No Telegram real send.
- No production config patch.
- Shadow replay is metadata-only.
- Board evidence freeze is metadata-only.
- Final dry-admission gate is not activation.
- Not investment advice.
"""

def build_dry_admission_review_from_parts(
    gate: FinalPaperModeDryAdmissionGate,
    replay_result: ShadowLaunchReplayResult | None = None,
    freeze_bundle: BoardEvidenceFreezeBundle | None = None
) -> DryAdmissionGateFullReview:
    return DryAdmissionGateFullReview(
        review_id=create_dry_admission_full_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=DryAdmissionGateReportType.FULL_DRY_ADMISSION_GATE_REVIEW,
        gates=[gate],
        shadow_replay_plans=[],
        shadow_replay_results=[replay_result] if replay_result else [],
        shadow_replay_items=[],
        evidence_freezes=[freeze_bundle] if freeze_bundle else [],
        rules=gate.rules,
        assertions=gate.assertions,
        audit_entries=[],
        output_paths={},
        warnings=[],
        errors=[]
    )

def build_dry_admission_gate_full_review(board_payload: dict[str, Any]) -> DryAdmissionGateFullReview:
    from usa_signal_bot.paper_mode_dry_admission_gate.final_dry_admission_gate import build_final_paper_mode_dry_admission_gate
    gate = build_final_paper_mode_dry_admission_gate(board_payload)
    return build_dry_admission_review_from_parts(gate)

def dry_admission_gate_full_review_summary(review: DryAdmissionGateFullReview) -> dict[str, Any]:
    gate = review.gates[-1] if review.gates else None
    return {
        "review_id": review.review_id,
        "gate_status": gate.status.value if gate else "NONE",
        "gate_passed": gate.dry_admission_gate_passed if gate else False
    }

def dry_admission_gate_full_review_to_text(review: DryAdmissionGateFullReview, limit: int = 100) -> str:
    summary = dry_admission_gate_full_review_summary(review)
    return f"Dry Admission Full Review {summary['review_id']}\nPassed: {summary['gate_passed']}\n{dry_admission_gate_limitations_text()}"
