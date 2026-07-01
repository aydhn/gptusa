import pytest
from unittest.mock import MagicMock
from usa_signal_bot.attribution.attribution_models import (
    AttributionReview,
    RiskAttributionContribution,
)
from usa_signal_bot.core.enums import (
    AttributionDimension,
    RiskContributionType,
    ContributionDirection,
)
from usa_signal_bot.attribution.risk_adapter import (
    attach_attribution_to_risk_report,
    attribution_risk_warnings,
)


def _get_mock_review():
    risk_contrib = RiskAttributionContribution(
        contribution_id="c1",
        risk_type=RiskContributionType.DRAWDOWN,
        dimension=AttributionDimension.SYMBOL,
        name="AAPL",
        drawdown_contribution_usd=50.0,
        contribution_direction=ContributionDirection.NEGATIVE,
    )
    return AttributionReview(
        review_id="r1",
        created_at_utc="now",
        report_type=None,
        events=[],
        performance_contributions=[],
        risk_contributions=[risk_contrib],
        signal_contributions=[],
    )


def test_attach_attribution_to_risk_report():
    payload = {"status": "ok"}
    review = _get_mock_review()
    attached = attach_attribution_to_risk_report(payload, review)
    assert "attribution_metadata" in attached
    assert "risk_summary" in attached["attribution_metadata"]


def test_attribution_risk_warnings_with_high_risk():
    review = _get_mock_review()
    review.scorecard = MagicMock()
    review.scorecard.high_risk_contributor_count = 5
    warnings = attribution_risk_warnings(review)
    assert warnings == ["Found 5 high risk contributors."]


def test_attribution_risk_warnings_with_zero_high_risk():
    review = _get_mock_review()
    review.scorecard = MagicMock()
    review.scorecard.high_risk_contributor_count = 0
    warnings = attribution_risk_warnings(review)
    assert warnings == []


def test_attribution_risk_warnings_no_scorecard():
    review = _get_mock_review()
    review.scorecard = None
    warnings = attribution_risk_warnings(review)
    assert warnings == []
