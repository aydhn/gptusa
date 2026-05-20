from typing import Any
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import (
    DryRunBridgeContext,
    DryRunProposal,
    BridgeTelemetryEvent,
    HumanReviewCheckpoint,
    DryRunBridgeSession,
    DryRunBridgeReview
)

def dry_run_bridge_limitations_text() -> str:
    return (
        "NOTE: Dry-run bridge is NOT active paper trading.\n"
        "Proposals are NOT real orders.\n"
        "Human checkpoints are NOT deployment approvals.\n"
        "Bridge telemetry is strictly local.\n"
        "No broker/live/demo orders are generated.\n"
        "No real paper mutation occurs.\n"
        "No Telegram real send.\n"
        "No production config patches.\n"
        "This is NOT investment advice."
    )

def dry_run_context_to_text(item: DryRunBridgeContext) -> str:
    return f"Context {item.context_id} (Mode: {item.mode.value})"

def dry_run_proposal_to_text(item: DryRunProposal) -> str:
    return f"Proposal {item.proposal_id} ({item.proposal_type.value}) - Status: {item.status.value}"

def bridge_telemetry_event_to_text(item: BridgeTelemetryEvent) -> str:
    return f"Telemetry {item.event_id} ({item.event_type.value})"

def human_review_checkpoint_to_text(item: HumanReviewCheckpoint) -> str:
    return f"Checkpoint {item.checkpoint_id} - Status: {item.status.value}"

def dry_run_bridge_session_to_text(item: DryRunBridgeSession, limit: int = 100) -> str:
    lines = [
        f"Session {item.session_id} - Status: {item.status.value}",
        f"Proposals: {len(item.proposals)}",
        f"Telemetry Events: {len(item.telemetry_events)}",
        f"Checkpoints: {len(item.human_checkpoints)}",
        dry_run_bridge_limitations_text()
    ]
    return "\n".join(lines)

def dry_run_bridge_review_to_text(item: DryRunBridgeReview, limit: int = 100) -> str:
    lines = [
        f"Review {item.review_id} - Report Type: {item.report_type.value}",
        f"Sessions: {len(item.sessions)}",
        f"Total Telemetry Events: {len(item.telemetry_events)}",
        dry_run_bridge_limitations_text()
    ]
    return "\n".join(lines)

def dry_run_bridge_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Store Summary: {summary.get('sessions', 0)} sessions, {summary.get('reviews', 0)} reviews."
