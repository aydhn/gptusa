import datetime
from typing import Any
from usa_signal_bot.core.enums import IncidentStatus
from usa_signal_bot.incident.incident_models import IncidentRecord, IncidentTimelineEvent, create_incident_timeline_event_id

def build_incident_timeline(incidents: list[IncidentRecord]) -> list[IncidentTimelineEvent]:
    timeline = []
    for inc in incidents:
        timeline.append(
            IncidentTimelineEvent(
                event_id=create_incident_timeline_event_id(),
                incident_id=inc.incident_id,
                timestamp_utc=inc.created_at_utc,
                status=inc.status,
                message=f"Incident '{inc.title}' raised.",
                source=inc.source,
                evidence=inc.evidence.get("summary_snippet", {})
            )
        )
    return sort_incident_timeline(timeline)

def append_timeline_event(timeline: list[IncidentTimelineEvent], incident: IncidentRecord, status: IncidentStatus, message: str) -> list[IncidentTimelineEvent]:
    new_timeline = list(timeline)
    new_timeline.append(
         IncidentTimelineEvent(
            event_id=create_incident_timeline_event_id(),
            incident_id=incident.incident_id,
            timestamp_utc=datetime.datetime.utcnow().isoformat() + "Z",
            status=status,
            message=message,
            source=incident.source,
            evidence={}
         )
    )
    return sort_incident_timeline(new_timeline)

def sort_incident_timeline(timeline: list[IncidentTimelineEvent]) -> list[IncidentTimelineEvent]:
    return sorted(timeline, key=lambda x: x.timestamp_utc)

def incident_timeline_to_text(timeline: list[IncidentTimelineEvent], limit: int = 50) -> str:
    lines = []
    for t in timeline[-limit:]:
        lines.append(f"[{t.timestamp_utc}] {t.status.name} ({t.source.name}): {t.message}")
    if not lines:
        return "Timeline empty."
    return "\n".join(lines)

def group_incidents_by_source(incidents: list[IncidentRecord]) -> dict[str, int]:
    counts = {}
    for i in incidents:
        counts[i.source.value] = counts.get(i.source.value, 0) + 1
    return counts

def group_incidents_by_severity(incidents: list[IncidentRecord]) -> dict[str, int]:
    counts = {}
    for i in incidents:
        counts[i.severity.value] = counts.get(i.severity.value, 0) + 1
    return counts
