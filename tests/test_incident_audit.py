from usa_signal_bot.incident.incident_audit import create_incident_audit_event
def test_create_audit():
    e = create_incident_audit_event("TEST", "OK", "msg", None, "/some/secret/path")
    assert e.path == "[REDACTED_SENSITIVE_PATH]"
