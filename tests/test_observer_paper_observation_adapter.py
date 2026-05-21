from usa_signal_bot.paper_observer.paper_observation_adapter import (
    observer_requirements_from_observation_review,
    observation_supports_observer_enrollment,
    attach_observer_hint_to_observation_payload
)
from usa_signal_bot.paper_observer.observer_report import build_paper_observer_review
from usa_signal_bot.paper_observer.observer_enrollment import build_observer_enrollment

def test_paper_observation_adapter():
    reqs = observer_requirements_from_observation_review({})
    assert reqs["requires_locked_runtime"] is True

    supports, _ = observation_supports_observer_enrollment({"status": "OK"})
    assert supports is True

    supports, warnings = observation_supports_observer_enrollment({"status": "REJECTED"})
    assert supports is False
    assert len(warnings) == 1

    enrollment = build_observer_enrollment("cand_1", "t1", "OK")
    review = build_paper_observer_review(enrollment)

    payload = attach_observer_hint_to_observation_payload({}, review)
    assert "paper_observer_hint" in payload
    assert payload["paper_observer_hint"]["review_id"] == review.review_id
