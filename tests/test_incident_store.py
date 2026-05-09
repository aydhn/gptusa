from usa_signal_bot.incident.incident_store import incident_store_summary
from pathlib import Path
def test_incident_store_summary(tmp_path):
    s = incident_store_summary(tmp_path)
    assert s["incident_reports_count"] == 0
