from typing import Any
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import (
    DryRunBridgeContext,
    DryRunBridgeSession,
    DryRunBridgeReview
)
from usa_signal_bot.paper_dry_run_bridge.dry_run_context import build_dry_run_bridge_context
from usa_signal_bot.paper_dry_run_bridge.bridge_session_runner import SupervisedDryRunBridgeRunner
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import create_dry_run_bridge_review_id, DryRunBridgeReportType
from datetime import datetime, timezone

def dry_run_context_from_quarantine_review(payload: dict[str, Any]) -> DryRunBridgeContext:
    # A generic implementation to bridge Phase 72 review into a context
    return build_dry_run_bridge_context(quarantine_payload=payload)

def dry_run_session_from_quarantine_review(payload: dict[str, Any]) -> DryRunBridgeSession:
    context = dry_run_context_from_quarantine_review(payload)
    runner = SupervisedDryRunBridgeRunner()
    return runner.run_session(context)

def dry_run_review_from_quarantine_review(payload: dict[str, Any]) -> DryRunBridgeReview:
    session = dry_run_session_from_quarantine_review(payload)
    return DryRunBridgeReview(
        review_id=create_dry_run_bridge_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=DryRunBridgeReportType.FULL_DRY_RUN_BRIDGE_REVIEW,
        sessions=[session],
        telemetry_events=session.telemetry_events,
        checkpoints=session.human_checkpoints,
        output_paths=session.output_paths,
        warnings=session.warnings,
        errors=session.errors
    )

def attach_dry_run_metadata_to_quarantine_payload(payload: dict[str, Any], review: DryRunBridgeReview) -> dict[str, Any]:
    result = payload.copy()
    result["dry_run_bridge_metadata"] = {
        "review_id": review.review_id,
        "completed": True,
        "errors_count": len(review.errors)
    }
    return result

def paper_quarantine_dry_run_summary(payload: dict[str, Any]) -> dict[str, Any]:
    metadata = payload.get("dry_run_bridge_metadata", {})
    return {
        "has_dry_run_metadata": bool(metadata),
        "review_id": metadata.get("review_id")
    }

def paper_quarantine_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = paper_quarantine_dry_run_summary(payload)
    return f"Quarantine Adapter: DryRun Attached={summary['has_dry_run_metadata']}"
