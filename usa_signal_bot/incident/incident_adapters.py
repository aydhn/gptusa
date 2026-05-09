from pathlib import Path
from typing import Any
import datetime
import json
from usa_signal_bot.core.enums import IncidentSeverity, IncidentSource, IncidentCategory, IncidentStatus
from usa_signal_bot.incident.incident_models import IncidentRecord, create_incident_id
from usa_signal_bot.incident.incident_classifier import (
    classify_incident_severity, classify_incident_category_from_message,
    incident_status_from_evidence, build_incident_title, classify_incident_source_from_record
)

def incident_from_observability_event(event: dict[str, Any]) -> IncidentRecord | None:
    if event.get("level", "").upper() not in ["ERROR", "CRITICAL", "WARNING"]:
        return None

    source = classify_incident_source_from_record(event)
    message = event.get("message", "Unknown observability error")
    category = classify_incident_category_from_message(message)
    severity = classify_incident_severity(source, category, event)

    if event.get("level", "").upper() == "WARNING" and severity_rank(severity) > severity_rank(IncidentSeverity.MEDIUM):
        severity = IncidentSeverity.MEDIUM

    return IncidentRecord(
        incident_id=create_incident_id("obs"),
        title=build_incident_title(source, category, event),
        severity=severity,
        status=IncidentStatus.OPEN,
        source=source,
        category=category,
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        updated_at_utc=None,
        summary=message,
        evidence=event
    )

def incidents_from_observability_events(events: list[dict[str, Any]]) -> list[IncidentRecord]:
    incs = []
    for e in events:
        inc = incident_from_observability_event(e)
        if inc:
            incs.append(inc)
    return incs

def incident_from_operational_health_report(report: dict[str, Any]) -> list[IncidentRecord]:
    incs = []
    if report.get("status") in ["unhealthy", "degraded"]:
        ev = report
        source = IncidentSource.OBSERVABILITY
        category = IncidentCategory.RUNTIME_FAILURE
        severity = IncidentSeverity.CRITICAL if report.get("status") == "unhealthy" else IncidentSeverity.HIGH
        incs.append(IncidentRecord(
            incident_id=create_incident_id("health"),
            title=f"Health Report {report.get('status', 'issue')}",
            severity=severity,
            status=IncidentStatus.OPEN,
            source=source,
            category=category,
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            updated_at_utc=None,
            summary="Operational health check reported an issue.",
            evidence=ev
        ))
    return incs

def incident_from_quality_acceptance_result(result: dict[str, Any]) -> list[IncidentRecord]:
    incs = []
    if result.get("status") == "blocked":
        ev = result
        incs.append(IncidentRecord(
            incident_id=create_incident_id("qual"),
            title=build_incident_title(IncidentSource.QUALITY, IncidentCategory.QUALITY_GATE_FAILURE, ev),
            severity=classify_incident_severity(IncidentSource.QUALITY, IncidentCategory.QUALITY_GATE_FAILURE, ev),
            status=IncidentStatus.BLOCKED,
            source=IncidentSource.QUALITY,
            category=IncidentCategory.QUALITY_GATE_FAILURE,
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            updated_at_utc=None,
            summary="Quality acceptance blocked.",
            evidence=ev
        ))
    return incs

def incident_from_regression_result(result: dict[str, Any]) -> list[IncidentRecord]:
    incs = []
    if result.get("status") in ["failed", "blocked"]:
        ev = result
        incs.append(IncidentRecord(
            incident_id=create_incident_id("regr"),
            title=build_incident_title(IncidentSource.REGRESSION, IncidentCategory.REGRESSION_FAILURE, ev),
            severity=classify_incident_severity(IncidentSource.REGRESSION, IncidentCategory.REGRESSION_FAILURE, ev),
            status=IncidentStatus.BLOCKED if result.get("status") == "blocked" else IncidentStatus.OPEN,
            source=IncidentSource.REGRESSION,
            category=IncidentCategory.REGRESSION_FAILURE,
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            updated_at_utc=None,
            summary="Regression test failed or blocked.",
            evidence=ev
        ))
    return incs

def incident_from_release_result(result: dict[str, Any]) -> list[IncidentRecord]:
    incs = []
    if result.get("status") != "success" or result.get("include_secrets", False):
        ev = result
        cat = IncidentCategory.SECRET_LEAK_RISK if result.get("include_secrets") else IncidentCategory.RELEASE_FAILURE
        incs.append(IncidentRecord(
            incident_id=create_incident_id("rel"),
            title=build_incident_title(IncidentSource.RELEASE, cat, ev),
            severity=classify_incident_severity(IncidentSource.RELEASE, cat, ev),
            status=IncidentStatus.BLOCKED,
            source=IncidentSource.RELEASE,
            category=cat,
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            updated_at_utc=None,
            summary="Release generation failed or contained secrets.",
            evidence=ev
        ))
    return incs

def incident_from_retention_result(result: dict[str, Any]) -> list[IncidentRecord]:
    incs = []
    if result.get("status") == "failed" or any("protected" in str(w).lower() for w in result.get("warnings", [])):
        ev = result
        cat = IncidentCategory.SAFETY_VIOLATION if "protected" in str(result).lower() else IncidentCategory.RETENTION_FAILURE
        incs.append(IncidentRecord(
            incident_id=create_incident_id("ret"),
            title=build_incident_title(IncidentSource.RETENTION, cat, ev),
            severity=classify_incident_severity(IncidentSource.RETENTION, cat, ev),
            status=IncidentStatus.BLOCKED if cat == IncidentCategory.SAFETY_VIOLATION else IncidentStatus.OPEN,
            source=IncidentSource.RETENTION,
            category=cat,
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            updated_at_utc=None,
            summary="Retention task failed or violated protected paths.",
            evidence=ev
        ))
    return incs

def incident_from_disk_quota_report(report: dict[str, Any]) -> list[IncidentRecord]:
    incs = []
    if report.get("exceeded") or report.get("critical"):
        ev = report
        incs.append(IncidentRecord(
            incident_id=create_incident_id("quota"),
            title=build_incident_title(IncidentSource.STORAGE, IncidentCategory.DISK_QUOTA, ev),
            severity=classify_incident_severity(IncidentSource.STORAGE, IncidentCategory.DISK_QUOTA, ev),
            status=IncidentStatus.OPEN,
            source=IncidentSource.STORAGE,
            category=IncidentCategory.DISK_QUOTA,
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            updated_at_utc=None,
            summary="Disk quota exceeded or critical.",
            evidence=ev
        ))
    return incs

def incident_from_validation_report(report: dict[str, Any], source: IncidentSource) -> list[IncidentRecord]:
    incs = []
    if not report.get("valid", True):
        ev = report
        incs.append(IncidentRecord(
            incident_id=create_incident_id("val"),
            title=build_incident_title(source, IncidentCategory.VALIDATION_FAILURE, ev),
            severity=IncidentSeverity.HIGH,
            status=IncidentStatus.OPEN,
            source=source,
            category=IncidentCategory.VALIDATION_FAILURE,
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            updated_at_utc=None,
            summary="Validation report indicates failure.",
            evidence=ev
        ))
    return incs

def collect_incidents_from_latest_artifacts(data_root: Path) -> list[IncidentRecord]:
    incs = []
    def _read_latest(pattern, d_path):
        import fnmatch
        import os
        if not d_path.exists():
             return None
        files = [f for f in d_path.iterdir() if f.is_file() and fnmatch.fnmatch(f.name, pattern)]
        if not files:
            return None
        latest = max(files, key=os.path.getmtime)
        try:
            with open(latest, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None

    # This is a heuristic collection, missing files are expected
    obs_err = _read_latest("errors*.jsonl", data_root / "observability")
    # simulate list read for jsonl
    if obs_err is None and (data_root / "observability").exists():
        files = list((data_root / "observability").glob("errors*.jsonl"))
        if files:
            latest = max(files, key=lambda f: f.stat().st_mtime)
            try:
                events = []
                with open(latest, 'r', encoding='utf-8') as f:
                    for line in f:
                         if line.strip():
                             events.append(json.loads(line))
                incs.extend(incidents_from_observability_events(events))
            except:
                pass

    hq = _read_latest("health*.json", data_root / "observability")
    if hq:
         incs.extend(incident_from_operational_health_report(hq))

    qa = _read_latest("quality_report*.json", data_root / "quality")
    if qa:
        incs.extend(incident_from_quality_acceptance_result(qa))

    reg = _read_latest("regression*.json", data_root / "regression")
    if reg:
        incs.extend(incident_from_regression_result(reg))

    rel = _read_latest("release*.json", data_root / "release")
    if rel:
        incs.extend(incident_from_release_result(rel))

    ret = _read_latest("retention*.json", data_root / "retention")
    if ret:
        incs.extend(incident_from_retention_result(ret))

    return incs

def severity_rank(severity: IncidentSeverity) -> int:
    from usa_signal_bot.incident.incident_classifier import severity_rank as sr
    return sr(severity)
