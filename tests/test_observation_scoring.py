from usa_signal_bot.paper_observation.observation_models import ObservationWindow, ObservationTelemetrySummary, CheckpointHistoryEntry, ObservationScoreStatus, ObservationRiskFlag
from usa_signal_bot.paper_observation.observation_scoring import build_observation_scorecard, observation_scorecard_to_text
import datetime

def test_observation_scoring():
    window = ObservationWindow("w1", "2023", "c1", "t1", "PLANNED", "FULL_SUPERVISED_OBSERVATION", None, None, 3, 3, [], [], 0, 0, False)
    telemetry = ObservationTelemetrySummary("t1", "2023", "w1", "c1", 10, 3, 3, 0, 0, 0, 0, 0)
    cp = CheckpointHistoryEntry("h1", datetime.datetime.now(datetime.timezone.utc).isoformat(), "cp1", "s1", "c1", "t1", "REVIEWED", None, None)

    sc = build_observation_scorecard(window, telemetry, [cp], [])
    assert sc.status == ObservationScoreStatus.PASS
    assert sc.score == 100.0

    # Missing session
    window.observed_session_count = 1
    sc2 = build_observation_scorecard(window, telemetry, [cp], [])
    assert sc2.status == ObservationScoreStatus.PASS
    assert sc2.score == 80.0
    assert ObservationRiskFlag.INSUFFICIENT_DRY_RUN_SESSIONS in sc2.risk_flags

    # Blocked operation (safety risk)
    telemetry.blocked_operation_count = 1
    sc3 = build_observation_scorecard(window, telemetry, [cp], [{"real_order_risk_detected": True}])
    assert sc3.status == ObservationScoreStatus.BLOCKED
    assert ObservationRiskFlag.REAL_ORDER_RISK in sc3.risk_flags

    text = observation_scorecard_to_text(sc)
    assert "100.0" in text
