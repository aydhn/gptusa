from typing import Any, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import PrePaperHandoffFreezeReportType
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_models import (
    PrePaperHandoffFreezeFullReview,
    FinalPrePaperHandoffFreezeGate,
    SandboxRuntimeAdmissionReplayResult,
    SimulatorEvidenceFreezeBundle,
    create_handoff_freeze_full_review_id
)

def build_handoff_freeze_full_review(payload: dict[str, Any]) -> PrePaperHandoffFreezeFullReview:
    return PrePaperHandoffFreezeFullReview(
        review_id=create_handoff_freeze_full_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=PrePaperHandoffFreezeReportType.FULL_PRE_PAPER_HANDOFF_FREEZE_REVIEW,
        gates=payload.get("gates", []),
        sandbox_replay_plans=payload.get("sandbox_replay_plans", []),
        sandbox_replay_results=payload.get("sandbox_replay_results", []),
        sandbox_replay_items=payload.get("sandbox_replay_items", []),
        evidence_freezes=payload.get("evidence_freezes", []),
        rules=payload.get("rules", []),
        assertions=payload.get("assertions", []),
        audit_entries=payload.get("audit_entries", []),
        output_paths=payload.get("output_paths", {}),
        warnings=payload.get("warnings", []),
        errors=payload.get("errors", [])
    )

def build_handoff_freeze_review_from_parts(
    gate: FinalPrePaperHandoffFreezeGate,
    replay_result: Optional[SandboxRuntimeAdmissionReplayResult] = None,
    freeze_bundle: Optional[SimulatorEvidenceFreezeBundle] = None
) -> PrePaperHandoffFreezeFullReview:

    review = build_handoff_freeze_full_review({
        "gates": [gate],
        "rules": gate.rules,
        "assertions": gate.assertions
    })

    if replay_result:
        review.sandbox_replay_results.append(replay_result)

    if freeze_bundle:
        review.evidence_freezes.append(freeze_bundle)

    return review

def handoff_freeze_full_review_summary(review: PrePaperHandoffFreezeFullReview) -> dict[str, Any]:
    return {
        "review_id": review.review_id,
        "gate_count": len(review.gates),
        "replay_result_count": len(review.sandbox_replay_results),
        "evidence_freeze_count": len(review.evidence_freezes)
    }

def handoff_freeze_limitations_text() -> str:
    return (
        "Phase 100 Limitations:\n"
        "- no broker/live/demo order\n"
        "- no active paper enable\n"
        "- no paper admission\n"
        "- no simulator admission\n"
        "- no local paper simulator start\n"
        "- no paper sandbox runtime admission\n"
        "- no paper sandbox runtime start\n"
        "- no real paper mutation\n"
        "- no paper order\n"
        "- no Telegram real send\n"
        "- no production config patch\n"
        "- sandbox runtime admission replay is metadata-only\n"
        "- simulator evidence freeze is metadata-only\n"
        "- final pre-paper handoff freeze gate is not activation\n"
        "- Phase 101+ transition requires separate explicit development\n"
        "- not investment advice"
    )

def handoff_freeze_full_review_to_text(review: PrePaperHandoffFreezeFullReview, limit: int = 100) -> str:
    res = f"Handoff Freeze Full Review: {review.review_id}\n"
    res += f"Gates: {len(review.gates)}\n"
    res += f"Replay Results: {len(review.sandbox_replay_results)}\n"
    res += f"Evidence Freezes: {len(review.evidence_freezes)}\n"
    res += "\n" + handoff_freeze_limitations_text()
    return res
