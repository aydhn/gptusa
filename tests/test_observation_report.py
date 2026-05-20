from usa_signal_bot.paper_observation.observation_models import ObservationWindow, ObservationTelemetrySummary, CheckpointHistoryEntry
from usa_signal_bot.paper_observation.observation_report import build_quarantine_exit_review, build_observation_review, observation_review_summary, observation_limitations_text, observation_review_to_text
import datetime

def test_observation_report():
    window = ObservationWindow("w1", "2023", "c1", "t1", "PLANNED", "FULL_SUPERVISED_OBSERVATION", None, None, 3, 3, [], [], 0, 0, False)
    telemetry = ObservationTelemetrySummary("t1", "2023", "w1", "c1", 10, 3, 3, 0, 0, 0, 0, 0)
    cp = CheckpointHistoryEntry("h1", datetime.datetime.now(datetime.timezone.utc).isoformat(), "cp1", "s1", "c1", "t1", "REVIEWED", None, None)

    exit_rev = build_quarantine_exit_review(window, telemetry, [cp])
    assert exit_rev.decision == "ELIGIBLE_FOR_CONTROLLED_PAPER_OBSERVATION_PLANNING"

    obs_rev = build_observation_review(window, None, None)
    assert len(obs_rev.exit_reviews) == 1

    summ = observation_review_summary(obs_rev)
    assert "exit_decision" in summ

    lim = observation_limitations_text()
    assert "NOT investment advice" in lim

    text = observation_review_to_text(obs_rev)
    assert "Observation Review" in text
