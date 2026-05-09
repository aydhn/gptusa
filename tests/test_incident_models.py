import pytest
from usa_signal_bot.core.enums import IncidentSeverity, IncidentStatus, IncidentSource, IncidentCategory, IncidentReportType
from usa_signal_bot.incident.incident_models import IncidentRecord, IncidentTimelineEvent, IncidentSummaryReport, validate_incident_record, create_incident_id
from usa_signal_bot.core.exceptions import IncidentValidationError

def test_incident_record_valid():
    rec = IncidentRecord(
        incident_id=create_incident_id(),
        title="Test",
        severity=IncidentSeverity.LOW,
        status=IncidentStatus.OPEN,
        source=IncidentSource.RUNTIME,
        category=IncidentCategory.RUNTIME_FAILURE,
        created_at_utc="2024-01-01T00:00:00Z",
        updated_at_utc=None,
        summary="Test summary"
    )
    validate_incident_record(rec)

def test_incident_record_empty_title():
    rec = IncidentRecord(
        incident_id=create_incident_id(),
        title="",
        severity=IncidentSeverity.LOW,
        status=IncidentStatus.OPEN,
        source=IncidentSource.RUNTIME,
        category=IncidentCategory.RUNTIME_FAILURE,
        created_at_utc="2024-01-01T00:00:00Z",
        updated_at_utc=None,
        summary="Test summary"
    )
    with pytest.raises(IncidentValidationError, match="Title cannot be empty"):
        validate_incident_record(rec)

def test_incident_record_secret_evidence():
    rec = IncidentRecord(
        incident_id=create_incident_id(),
        title="Test",
        severity=IncidentSeverity.LOW,
        status=IncidentStatus.OPEN,
        source=IncidentSource.RUNTIME,
        category=IncidentCategory.RUNTIME_FAILURE,
        created_at_utc="2024-01-01T00:00:00Z",
        updated_at_utc=None,
        summary="Test summary",
        evidence={"my_secret": "value"}
    )
    with pytest.raises(IncidentValidationError, match="Evidence may contain sensitive token"):
        validate_incident_record(rec)
