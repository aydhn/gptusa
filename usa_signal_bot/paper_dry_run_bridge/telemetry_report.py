from typing import Any
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import DryRunBridgeSession
from usa_signal_bot.paper_dry_run_bridge.telemetry_collector import telemetry_collector_summary
from usa_signal_bot.paper_dry_run_bridge.blocked_operation_telemetry import blocked_operation_telemetry_summary

def build_bridge_telemetry_report(session: DryRunBridgeSession) -> dict[str, Any]:
    context = session.context
    return {
        "session_id": session.session_id,
        "candidate_id": context.candidate_id if context else None,
        "ticket_id": context.ticket_id if context else None,
        "telemetry_summary": telemetry_collector_summary(session.telemetry_events),
        "blocked_operations": blocked_operation_telemetry_summary(session.telemetry_events),
        "safety_flags": [f.value for f in session.safety_flags],
        "human_checkpoints_count": len(session.human_checkpoints),
        "local_only_telemetry": True
    }

def bridge_telemetry_report_summary(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "session_id": report["session_id"],
        "total_events": report["telemetry_summary"]["total_events"],
        "blocked_operations": report["blocked_operations"]["count"]
    }

def bridge_telemetry_limitations_text() -> str:
    return "NOTE: Bridge telemetry is strictly local metadata. It is NOT external telemetry (like Prometheus/Datadog) and DOES NOT involve any broker API or real order execution logging."

def bridge_telemetry_report_to_text(report: dict[str, Any]) -> str:
    summary = bridge_telemetry_report_summary(report)
    return f"Telemetry Report for {summary['session_id']}: {summary['total_events']} events, {summary['blocked_operations']} blocked ops.\n{bridge_telemetry_limitations_text()}"
