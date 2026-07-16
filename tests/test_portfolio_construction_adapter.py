import pytest
import sys
from unittest.mock import MagicMock

# Create a clean mock structure specifically for testing this file isolated from global state
class StubEnumMember(str):
    def __init__(self, name):
        self.name = name
    @property
    def value(self):
        return self.name
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        return self.name == getattr(other, 'name', other)
    def __getattr__(self, attr):
        if attr in ("_is_protocol", "_mock_methods", "__class_getitem__", "__mro__", "__bases__"):
            raise AttributeError(attr)
        return StubEnumMember(attr)

class StubEnum:
    def __getattr__(self, name):
        if name in ("_is_protocol", "_mock_methods", "__class_getitem__", "__mro__", "__bases__"):
            raise AttributeError(name)
        return StubEnumMember(name)

# Provide mock dependencies before importing the adapter
sys.modules['usa_signal_bot.core.enums'] = StubEnum()
sys.modules['usa_signal_bot.core.exceptions'] = MagicMock()

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

# Clean up sys.modules
def teardown_module():
    if 'usa_signal_bot.core.enums' in sys.modules:
        del sys.modules['usa_signal_bot.core.enums']
    if 'usa_signal_bot.core.exceptions' in sys.modules:
        del sys.modules['usa_signal_bot.core.exceptions']
