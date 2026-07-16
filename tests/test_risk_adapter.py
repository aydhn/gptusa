from unittest.mock import MagicMock
from usa_signal_bot.attribution.risk_adapter import attribution_risk_summary

def test_attribution_risk_summary():
    mock_review = MagicMock()
    mock_review.risk_contributions = [1, 2, 3]
    result = attribution_risk_summary(mock_review)
    assert result == {"high_risk_contributors": 3}
