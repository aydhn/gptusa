from pathlib import Path
from typing import Dict, Any
from datetime import datetime, timezone
from usa_signal_bot.core.enums import AdvancedTransitionReportType
from usa_signal_bot.advanced_transition.phase101_models import AdvancedTransitionFullReview, create_advanced_transition_full_review_id
from usa_signal_bot.advanced_transition.handoff_freeze_ingestion import ingest_latest_handoff_freeze_from_store
from usa_signal_bot.advanced_transition.advanced_transition_context import build_advanced_transition_context

def build_advanced_transition_full_review(project_root: Path | None = None, config: Dict[str, Any] | None = None) -> AdvancedTransitionFullReview:
    root = project_root if project_root else Path.cwd()
    handoff = ingest_latest_handoff_freeze_from_store(root)
    context = build_advanced_transition_context(handoff, root, config)

    return AdvancedTransitionFullReview(
        review_id=create_advanced_transition_full_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=AdvancedTransitionReportType.FULL_PHASE101_REVIEW,
        handoff_ingestion=handoff,
        context=context,
        module_inventory=context.module_inventory,
        runtime_boundary_manifest=context.runtime_boundary_manifest,
        roadmap_items=context.roadmap_items,
        output_paths={"report": str(root / "data/advanced_transition/reviews")},
        warnings=[],
        errors=[]
    )

def advanced_transition_full_review_summary(review: AdvancedTransitionFullReview) -> Dict[str, Any]:
    return {"review_id": review.review_id, "ready": review.context.advanced_transition_ready}

def advanced_transition_limitations_text() -> str:
    return "Phase 101 is NOT activation. No broker API, no paper orders, no Telegram real send."

def advanced_transition_full_review_to_text(review: AdvancedTransitionFullReview, limit: int = 300) -> str:
    return f"Review ID: {review.review_id}\nType: {review.report_type.name}\nReady: {review.context.advanced_transition_ready}"
