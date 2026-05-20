from typing import Any, List
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import (
    DryRunBridgeSession,
    DryRunProposalStatus,
    HumanReviewCheckpointStatus
)
from usa_signal_bot.paper_dry_run_bridge.blocked_operation_telemetry import blocked_operation_count

def analyze_dry_run_bridge_session(session: DryRunBridgeSession) -> dict[str, Any]:
    return {
        "metrics": dry_run_session_metrics(session),
        "warning_flags": dry_run_session_warning_flags(session),
        "block_flags": dry_run_session_block_flags(session),
        "success_flags": dry_run_session_success_flags(session)
    }

def dry_run_session_metrics(session: DryRunBridgeSession) -> dict[str, Any]:
    return {
        "proposal_count": len(session.proposals),
        "risk_accepted_count": len([p for p in session.proposals if p.status == DryRunProposalStatus.RISK_ACCEPTED]),
        "risk_warning_count": len([p for p in session.proposals if p.status == DryRunProposalStatus.RISK_WARNING]),
        "risk_rejected_count": len([p for p in session.proposals if p.status == DryRunProposalStatus.RISK_REJECTED]),
        "blocked_proposal_count": len([p for p in session.proposals if p.status == DryRunProposalStatus.BLOCKED]),
        "telemetry_event_count": len(session.telemetry_events),
        "blocked_operation_count": blocked_operation_count(session.telemetry_events),
        "checkpoint_required_count": len([c for c in session.human_checkpoints if c.required]),
        "safety_flag_count": len(session.safety_flags)
    }

def dry_run_session_warning_flags(session: DryRunBridgeSession) -> List[str]:
    flags = []
    metrics = dry_run_session_metrics(session)
    if metrics["risk_warning_count"] > 0:
        flags.append("HAS_RISK_WARNINGS")
    if metrics["blocked_operation_count"] > 0:
        flags.append("HAS_BLOCKED_OPERATIONS")
    return flags

def dry_run_session_block_flags(session: DryRunBridgeSession) -> List[str]:
    flags = []
    metrics = dry_run_session_metrics(session)
    if metrics["blocked_proposal_count"] > 0:
        flags.append("HAS_BLOCKED_PROPOSALS")
    if session.status == "blocked":
        flags.append("SESSION_BLOCKED")
    return flags

def dry_run_session_success_flags(session: DryRunBridgeSession) -> List[str]:
    flags = []
    if session.status == "completed":
        flags.append("SESSION_COMPLETED")
    return flags

def dry_run_session_analyzer_to_text(payload: dict[str, Any]) -> str:
    metrics = payload.get("metrics", {})
    return f"Analyzer: {metrics.get('proposal_count', 0)} proposals, {metrics.get('blocked_operation_count', 0)} blocked operations."
