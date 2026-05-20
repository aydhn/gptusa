from usa_signal_bot.paper_observation.observation_models import ObservationWindow, ObservationTelemetrySummary, CheckpointHistoryEntry
from usa_signal_bot.paper_observation.exit_gates import default_quarantine_exit_gates, exit_gates_to_text
import datetime

def test_exit_gates():
    window = ObservationWindow("w1", "2023", "c1", "t1", "PLANNED", "FULL_SUPERVISED_OBSERVATION", None, None, 3, 3, [], [], 0, 0, False)
    telemetry = ObservationTelemetrySummary("t1", "2023", "w1", "c1", 10, 3, 3, 0, 0, 0, 0, 0)
    cp = CheckpointHistoryEntry("h1", datetime.datetime.now(datetime.timezone.utc).isoformat(), "cp1", "s1", "c1", "t1", "REVIEWED", None, None)

    gates = default_quarantine_exit_gates(window, telemetry, [cp], [])
    assert len(gates) == 4
    assert all(g["passed"] for g in gates)

    text = exit_gates_to_text(gates)
    assert "Quarantine Exit Gates" in text
    assert "PASS" in text
