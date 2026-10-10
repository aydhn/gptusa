import pytest
import sys
from unittest.mock import MagicMock

from usa_signal_bot.attribution.portfolio_construction_adapter import (
    attach_attribution_to_portfolio_construction_review
)

def test_attach_attribution_to_portfolio_construction_review():
    review_payload = {"existing_data": "value"}
    mock_review = MagicMock()
    mock_review.review_id = "test_review_123"

    # We ignore the return value and check the side-effect mutation
    attach_attribution_to_portfolio_construction_review(review_payload, mock_review)

    assert "attribution_metadata" in review_payload
    assert review_payload["attribution_metadata"]["review_id"] == "test_review_123"
    assert review_payload["existing_data"] == "value"
