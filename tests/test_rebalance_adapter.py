import pytest
from unittest.mock import MagicMock
from usa_signal_bot.attribution.rebalance_adapter import attach_attribution_to_rebalance_review

def test_attach_attribution_to_rebalance_review():
    review_payload = {}
    mock_review = MagicMock()
    mock_review.review_id = "test_review_123"

    attach_attribution_to_rebalance_review(review_payload, mock_review)

    assert "attribution_metadata" in review_payload
    assert review_payload["attribution_metadata"]["review_id"] == "test_review_123"
