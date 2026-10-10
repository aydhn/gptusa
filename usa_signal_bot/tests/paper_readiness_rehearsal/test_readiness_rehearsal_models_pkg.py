import pytest
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_models import ReadinessRehearsalReview

def test_readiness_rehearsal_review_initialization():
    review_id = "test_review_123"
    review = ReadinessRehearsalReview(review_id=review_id)

    assert review.review_id == review_id
    assert isinstance(review, ReadinessRehearsalReview)

def test_readiness_rehearsal_review_missing_review_id():
    with pytest.raises(TypeError):
        ReadinessRehearsalReview()
