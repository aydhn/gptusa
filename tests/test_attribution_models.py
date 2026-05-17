import pytest
from usa_signal_bot.attribution.attribution_models import (
    AttributionTradeEvent, AttributionContribution, RiskAttributionContribution,
    SignalContribution, AttributionScorecard, AttributionReview,
    validate_attribution_trade_event, validate_attribution_contribution,
    create_attribution_trade_event_id, create_attribution_contribution_id,
    attribution_trade_event_to_dict
)
from usa_signal_bot.core.enums import AttributionDimension, ContributionDirection, AttributionQuality, SignalContributionStatus, RiskContributionType, AttributionReportType
from usa_signal_bot.core.exceptions import AttributionValidationError

def test_attribution_trade_event_validation():
    event = AttributionTradeEvent(event_id="e1", symbol="AAPL", notional_usd=100.0, quantity=10, total_cost_usd=5.0)
    validate_attribution_trade_event(event)

    with pytest.raises(AttributionValidationError):
        validate_attribution_trade_event(AttributionTradeEvent(event_id="e2", symbol="", notional_usd=100.0))

    with pytest.raises(AttributionValidationError):
        validate_attribution_trade_event(AttributionTradeEvent(event_id="e3", symbol="AAPL", quantity=-1))

    with pytest.raises(AttributionValidationError):
        validate_attribution_trade_event(AttributionTradeEvent(event_id="e4", symbol="AAPL", total_cost_usd=-5.0))

def test_attribution_contribution_validation():
    contrib = AttributionContribution(
        contribution_id="c1", dimension=AttributionDimension.SYMBOL, name="AAPL",
        contribution_direction=ContributionDirection.POSITIVE, gross_pnl_usd=100, net_pnl_usd=90,
        total_cost_usd=10, trade_count=5, win_count=4, loss_count=1, win_rate=80.0
    )
    validate_attribution_contribution(contrib)

    with pytest.raises(AttributionValidationError):
        contrib_invalid = AttributionContribution(
            contribution_id="c2", dimension=AttributionDimension.SYMBOL, name="AAPL",
            contribution_direction=ContributionDirection.POSITIVE, gross_pnl_usd=100, net_pnl_usd=90,
            total_cost_usd=10, trade_count=-1, win_count=0, loss_count=0
        )
        validate_attribution_contribution(contrib_invalid)

    with pytest.raises(AttributionValidationError):
        contrib_invalid_wr = AttributionContribution(
            contribution_id="c3", dimension=AttributionDimension.SYMBOL, name="AAPL",
            contribution_direction=ContributionDirection.POSITIVE, gross_pnl_usd=100, net_pnl_usd=90,
            total_cost_usd=10, trade_count=1, win_count=0, loss_count=0, win_rate=150.0
        )
        validate_attribution_contribution(contrib_invalid_wr)

def test_factory_methods():
    assert create_attribution_trade_event_id("AAPL").startswith("ev_aapl_")
    assert create_attribution_contribution_id("Trend Alpha").startswith("contrib_trend_alpha_")

def test_serialization():
    event = AttributionTradeEvent(event_id="e1", symbol="AAPL")
    d = attribution_trade_event_to_dict(event)
    assert d["event_id"] == "e1"
    assert d["symbol"] == "AAPL"
