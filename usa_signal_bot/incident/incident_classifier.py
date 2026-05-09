from typing import Any
from usa_signal_bot.core.enums import IncidentSeverity, IncidentStatus, IncidentSource, IncidentCategory
from usa_signal_bot.incident.incident_models import IncidentRecord

def severity_rank(severity: IncidentSeverity) -> int:
    ranks = {
        IncidentSeverity.INFO: 0,
        IncidentSeverity.UNKNOWN: 1,
        IncidentSeverity.LOW: 2,
        IncidentSeverity.MEDIUM: 3,
        IncidentSeverity.HIGH: 4,
        IncidentSeverity.CRITICAL: 5,
        IncidentSeverity.BLOCKER: 6
    }
    return ranks.get(severity, 1)

def classify_incident_severity(source: IncidentSource, category: IncidentCategory, evidence: dict[str, Any]) -> IncidentSeverity:
    if category in [IncidentCategory.SAFETY_VIOLATION, IncidentCategory.SECRET_LEAK_RISK]:
        return IncidentSeverity.BLOCKER

    if category == IncidentCategory.DISK_QUOTA:
        exceeded = evidence.get("exceeded", False)
        critical = evidence.get("critical", False)
        if exceeded or critical:
            return IncidentSeverity.CRITICAL
        return IncidentSeverity.HIGH

    if category == IncidentCategory.QUALITY_GATE_FAILURE:
        if evidence.get("status") == "blocked":
            return IncidentSeverity.HIGH

    if category == IncidentCategory.REGRESSION_FAILURE:
        if evidence.get("status") in ["blocked", "failed"]:
            return IncidentSeverity.HIGH

    if category == IncidentCategory.RELEASE_FAILURE:
        if evidence.get("include_secrets", False):
            return IncidentSeverity.BLOCKER

    if category == IncidentCategory.STORAGE_FAILURE:
        return IncidentSeverity.HIGH

    if category == IncidentCategory.CONFIG_ERROR:
        return IncidentSeverity.HIGH

    if source == IncidentSource.RUNTIME and "warning" in str(evidence).lower():
        return IncidentSeverity.MEDIUM

    if category == IncidentCategory.DATA_MISSING and "optional" in str(evidence).lower():
        return IncidentSeverity.LOW

    # Default logic
    if "error" in str(evidence).lower() or "fail" in str(evidence).lower():
        return IncidentSeverity.HIGH

    return IncidentSeverity.MEDIUM

def classify_incident_category_from_message(message: str) -> IncidentCategory:
    msg = message.lower()
    if "config" in msg:
        return IncidentCategory.CONFIG_ERROR
    if "secret" in msg or "token" in msg or "leak" in msg:
        return IncidentCategory.SECRET_LEAK_RISK
    if "safety" in msg or "violation" in msg:
        return IncidentCategory.SAFETY_VIOLATION
    if "quota" in msg or "disk" in msg:
        return IncidentCategory.DISK_QUOTA
    if "missing" in msg and "data" in msg:
        return IncidentCategory.DATA_MISSING
    if "quality" in msg:
        return IncidentCategory.QUALITY_GATE_FAILURE
    if "regression" in msg:
        return IncidentCategory.REGRESSION_FAILURE
    if "release" in msg:
        return IncidentCategory.RELEASE_FAILURE
    if "storage" in msg:
        return IncidentCategory.STORAGE_FAILURE
    if "runtime" in msg:
        return IncidentCategory.RUNTIME_FAILURE
    if "retention" in msg or "cleanup" in msg:
        return IncidentCategory.RETENTION_FAILURE
    if "paper" in msg:
        return IncidentCategory.PAPER_FAILURE
    if "backtest" in msg:
        return IncidentCategory.BACKTEST_FAILURE
    return IncidentCategory.UNKNOWN

def classify_incident_source_from_path(path: str | None) -> IncidentSource:
    if not path:
        return IncidentSource.UNKNOWN
    p = path.lower()
    if "runtime" in p or "scan" in p:
        return IncidentSource.RUNTIME
    if "quality" in p:
        return IncidentSource.QUALITY
    if "regression" in p:
        return IncidentSource.REGRESSION
    if "release" in p:
        return IncidentSource.RELEASE
    if "retention" in p:
        return IncidentSource.RETENTION
    if "observability" in p or "health" in p:
        return IncidentSource.OBSERVABILITY
    if "config" in p:
        return IncidentSource.CONFIG
    if "storage" in p:
        return IncidentSource.STORAGE
    if "paper" in p:
        return IncidentSource.PAPER
    if "backtest" in p:
        return IncidentSource.BACKTEST
    return IncidentSource.UNKNOWN

def classify_incident_source_from_record(record: dict[str, Any]) -> IncidentSource:
    if "source" in record:
        try:
            return IncidentSource(record["source"])
        except ValueError:
            pass
    if "path" in record:
        return classify_incident_source_from_path(record["path"])
    return IncidentSource.UNKNOWN

def incident_status_from_evidence(evidence: dict[str, Any]) -> IncidentStatus:
    if evidence.get("mitigated", False):
        return IncidentStatus.MITIGATED
    if evidence.get("recovered", False):
        return IncidentStatus.RECOVERED
    if evidence.get("blocked", False) or evidence.get("status") == "blocked":
        return IncidentStatus.BLOCKED
    return IncidentStatus.OPEN

def build_incident_title(source: IncidentSource, category: IncidentCategory, evidence: dict[str, Any]) -> str:
    return f"Incident at {source.value}: {category.value}"

def should_block_recovery(record: IncidentRecord) -> bool:
    return severity_rank(record.severity) >= severity_rank(IncidentSeverity.CRITICAL)
