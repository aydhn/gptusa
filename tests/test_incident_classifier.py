from usa_signal_bot.core.enums import IncidentSeverity, IncidentSource, IncidentCategory
from usa_signal_bot.incident.incident_classifier import classify_incident_severity, classify_incident_category_from_message

def test_safety_violation_is_blocker():
    sev = classify_incident_severity(IncidentSource.RUNTIME, IncidentCategory.SAFETY_VIOLATION, {})
    assert sev == IncidentSeverity.BLOCKER

def test_disk_quota_critical():
    sev = classify_incident_severity(IncidentSource.STORAGE, IncidentCategory.DISK_QUOTA, {"critical": True})
    assert sev == IncidentSeverity.CRITICAL

def test_category_from_message():
    cat = classify_incident_category_from_message("There is a secret leak")
    assert cat == IncidentCategory.SECRET_LEAK_RISK
