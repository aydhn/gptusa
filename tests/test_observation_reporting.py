from usa_signal_bot.paper_observation.observation_reporting import observation_limitations_text, observation_review_to_text
from usa_signal_bot.paper_observation.observation_models import ObservationReview

def test_observation_reporting():
    assert "NOT investment advice" in observation_limitations_text()

    rev = ObservationReview("r1", "2023", "FULL_OBSERVATION_REVIEW", [], [], [], [], [], [], {})
    text = observation_review_to_text(rev)
    assert "Observation Review r1" in text
