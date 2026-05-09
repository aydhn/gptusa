from usa_signal_bot.incident.incident_models import IncidentRecord, create_incident_id
from usa_signal_bot.core.enums import IncidentSeverity, IncidentStatus, IncidentSource, IncidentCategory
from usa_signal_bot.incident.incident_timeline import build_incident_timeline

def test_build_timeline():
    inc = IncidentRecord(
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
    tl = build_incident_timeline([inc])
    assert len(tl) == 1
    assert tl[0].incident_id == inc.incident_id
