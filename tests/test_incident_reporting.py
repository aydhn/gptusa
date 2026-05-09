from usa_signal_bot.incident.incident_reporting import incident_limitations_text
def test_limitations():
    t = incident_limitations_text()
    assert "No broker API execution" in t
