import pytest
from usa_signal_bot.paper_final_handoff.final_handoff_models import FinalHandoffReview


def test_final_handoff_review_creation():
    review = FinalHandoffReview(review_id="review_123")
    assert review.review_id == "review_123"


def test_final_handoff_review_equality():
    review1 = FinalHandoffReview(review_id="review_123")
    review2 = FinalHandoffReview(review_id="review_123")
    review3 = FinalHandoffReview(review_id="review_456")

    assert review1 == review2
    assert review1 != review3


def test_final_handoff_review_repr():
    review = FinalHandoffReview(review_id="review_123")
    assert repr(review) == "FinalHandoffReview(review_id='review_123')"
