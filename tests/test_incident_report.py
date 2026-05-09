from pathlib import Path
from usa_signal_bot.incident.incident_report import IncidentReportBuilder
from usa_signal_bot.core.enums import IncidentStatus

def test_empty_incidents():
    builder = IncidentReportBuilder(Path("data"))
    rep = builder.build_from_incidents([])
    assert rep.status == IncidentStatus.CLOSED
