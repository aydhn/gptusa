from dataclasses import dataclass, field
from typing import Any
import uuid
import datetime
from usa_signal_bot.core.enums import IncidentSeverity, IncidentStatus, IncidentSource, IncidentCategory, IncidentReportType
from usa_signal_bot.core.exceptions import IncidentValidationError

@dataclass
class IncidentRecord:
    incident_id: str
    title: str
    severity: IncidentSeverity
    status: IncidentStatus
    source: IncidentSource
    category: IncidentCategory
    created_at_utc: str
    updated_at_utc: str | None
    summary: str
    evidence: dict[str, Any] = field(default_factory=dict)
    related_paths: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

@dataclass
class IncidentTimelineEvent:
    event_id: str
    incident_id: str
    timestamp_utc: str
    status: IncidentStatus
    message: str
    source: IncidentSource
    evidence: dict[str, Any] = field(default_factory=dict)

@dataclass
class IncidentSummaryReport:
    report_id: str
    created_at_utc: str
    report_type: IncidentReportType
    status: IncidentStatus
    highest_severity: IncidentSeverity
    incident_count: int
    open_count: int
    critical_count: int
    incidents: list[IncidentRecord]
    timeline: list[IncidentTimelineEvent]
    recommended_actions: list[str]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

def create_incident_id(prefix: str = "incident") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_incident_timeline_event_id(prefix: str = "incident_event") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_incident_report_id(prefix: str = "incident_report") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def _redact_dict(d: dict) -> dict:
    import json
    s = json.dumps(d)
    for term in ["secret", "token", "password", "api_key", "credential"]:
        if term in s.lower():
            # Very basic redaction
            return {"redacted": "Contains sensitive terms"}
    return d

def validate_incident_record(record: IncidentRecord) -> None:
    if not record.title:
        raise IncidentValidationError("Title cannot be empty")
    if not record.summary:
        raise IncidentValidationError("Summary cannot be empty")

    # ensure evidence token redacted
    import json
    ev_str = json.dumps(record.evidence).lower()
    for term in ["secret", "token", "password", "api_key", "credential"]:
        if term in ev_str and "redacted" not in ev_str:
            raise IncidentValidationError(f"Evidence may contain sensitive token: {term}")

def validate_incident_summary_report(report: IncidentSummaryReport) -> None:
    for inc in report.incidents:
        validate_incident_record(inc)

    import json
    rep_str = json.dumps(incident_summary_report_to_dict(report)).lower()
    for term in ["investment advice", "live approval", "live trade", "live order"]:
        if term in rep_str and "not " not in rep_str and "no " not in rep_str:
             raise IncidentValidationError(f"Report contains prohibited language: {term}")

def incident_record_to_dict(record: IncidentRecord) -> dict:
    return {
        "incident_id": record.incident_id,
        "title": record.title,
        "severity": record.severity.value,
        "status": record.status.value,
        "source": record.source.value,
        "category": record.category.value,
        "created_at_utc": record.created_at_utc,
        "updated_at_utc": record.updated_at_utc,
        "summary": record.summary,
        "evidence": _redact_dict(record.evidence),
        "related_paths": record.related_paths,
        "warnings": record.warnings,
        "errors": record.errors
    }

def incident_timeline_event_to_dict(event: IncidentTimelineEvent) -> dict:
    return {
        "event_id": event.event_id,
        "incident_id": event.incident_id,
        "timestamp_utc": event.timestamp_utc,
        "status": event.status.value,
        "message": event.message,
        "source": event.source.value,
        "evidence": _redact_dict(event.evidence)
    }

def incident_summary_report_to_dict(report: IncidentSummaryReport) -> dict:
    return {
        "report_id": report.report_id,
        "created_at_utc": report.created_at_utc,
        "report_type": report.report_type.value,
        "status": report.status.value,
        "highest_severity": report.highest_severity.value,
        "incident_count": report.incident_count,
        "open_count": report.open_count,
        "critical_count": report.critical_count,
        "incidents": [incident_record_to_dict(i) for i in report.incidents],
        "timeline": [incident_timeline_event_to_dict(e) for e in report.timeline],
        "recommended_actions": report.recommended_actions,
        "output_paths": report.output_paths,
        "warnings": report.warnings,
        "errors": report.errors
    }
