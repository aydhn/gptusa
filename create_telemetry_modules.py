import os
from pathlib import Path

FILES = {}

FILES["usa_signal_bot/paper_observation/telemetry_history.py"] = """\
from typing import Any, List, Dict
from usa_signal_bot.paper_observation.observation_models import ObservationTelemetrySummary, create_observation_telemetry_summary_id
import datetime

def count_telemetry_event_types(events: List[dict[str, Any]]) -> Dict[str, int]:
    counts = {}
    for ev in events:
        t = ev.get("event_type", "UNKNOWN")
        counts[t] = counts.get(t, 0) + 1
    return counts

def count_telemetry_safety_flags(events: List[dict[str, Any]]) -> Dict[str, int]:
    counts = {}
    for ev in events:
        for flag in ev.get("safety_flags", []):
            counts[flag] = counts.get(flag, 0) + 1
    return counts

def telemetry_history_warnings(events: List[dict[str, Any]]) -> List[str]:
    warnings = []
    blocked = sum(1 for e in events if e.get("event_type") == "BLOCKED_OPERATION")
    if blocked > 0:
        warnings.append(f"Found {blocked} blocked operations in telemetry history.")
    return warnings

def aggregate_bridge_telemetry_history(events: List[dict[str, Any]]) -> ObservationTelemetrySummary:
    session_ids = set()
    for ev in events:
        sid = ev.get("session_id")
        if sid:
            session_ids.add(sid)

    risk_warnings = sum(1 for e in events if e.get("event_type") == "RISK_WARNING")
    risk_rejected = sum(1 for e in events if e.get("event_type") == "RISK_REJECTED")
    blocked_count = sum(1 for e in events if e.get("event_type") == "BLOCKED_OPERATION")
    safety_flags = sum(len(e.get("safety_flags", [])) for e in events)
    notif_warnings = sum(1 for e in events if e.get("event_type") == "NOTIFICATION_WARNING")

    return ObservationTelemetrySummary(
        summary_id=create_observation_telemetry_summary_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        window_id=None,
        candidate_id=None,
        event_count=len(events),
        session_count=len(session_ids),
        proposal_count=sum(1 for e in events if e.get("event_type") == "PROPOSAL"),
        risk_warning_count=risk_warnings,
        risk_rejected_count=risk_rejected,
        blocked_operation_count=blocked_count,
        safety_flag_count=safety_flags,
        notification_warning_count=notif_warnings,
        warnings=telemetry_history_warnings(events),
        errors=[],
        metadata={"event_types": count_telemetry_event_types(events)}
    )

def telemetry_history_to_text(summary: ObservationTelemetrySummary) -> str:
    return f"Telemetry Summary: {summary.summary_id}\\nEvents: {summary.event_count}\\nBlocked: {summary.blocked_operation_count}"
"""

FILES["usa_signal_bot/paper_observation/proposal_history.py"] = """\
from typing import Any, List, Dict

def count_proposals_by_type(sessions: List[dict[str, Any]]) -> Dict[str, int]:
    counts = {}
    for s in sessions:
        for p in s.get("proposals", []):
            t = p.get("type", "UNKNOWN")
            counts[t] = counts.get(t, 0) + 1
    return counts

def count_proposals_by_status(sessions: List[dict[str, Any]]) -> Dict[str, int]:
    counts = {}
    for s in sessions:
        for p in s.get("proposals", []):
            st = p.get("status", "UNKNOWN")
            counts[st] = counts.get(st, 0) + 1
    return counts

def proposal_history_warnings(sessions: List[dict[str, Any]]) -> List[str]:
    warnings = []
    st_counts = count_proposals_by_status(sessions)
    if st_counts.get("BLOCKED", 0) > 0:
        warnings.append(f"{st_counts['BLOCKED']} proposals were blocked.")
    return warnings

def aggregate_proposal_history(sessions: List[dict[str, Any]]) -> dict[str, Any]:
    total = 0
    for s in sessions:
        total += len(s.get("proposals", []))

    return {
        "total_proposals": total,
        "by_type": count_proposals_by_type(sessions),
        "by_status": count_proposals_by_status(sessions),
        "warnings": proposal_history_warnings(sessions)
    }

def proposal_history_to_text(payload: dict[str, Any]) -> str:
    return f"Proposal History\\nTotal: {payload.get('total_proposals', 0)}\\nWarnings: {len(payload.get('warnings', []))}"
"""

for file_path, content in FILES.items():
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {file_path}")
