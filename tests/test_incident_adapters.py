from usa_signal_bot.incident.incident_adapters import incident_from_observability_event, incident_from_operational_health_report
from usa_signal_bot.core.enums import IncidentSeverity

def test_incident_from_observability_error():
    ev = {"level": "ERROR", "message": "Runtime fail", "source": "RUNTIME"}
    inc = incident_from_observability_event(ev)
    assert inc is not None
    assert inc.severity == IncidentSeverity.HIGH

def test_incident_from_obs_info():
    ev = {"level": "INFO", "message": "All good"}
    inc = incident_from_observability_event(ev)
    assert inc is None

def test_incident_from_health_unhealthy():
    rep = {"status": "unhealthy"}
    incs = incident_from_operational_health_report(rep)
    assert len(incs) == 1
    assert incs[0].severity == IncidentSeverity.CRITICAL
