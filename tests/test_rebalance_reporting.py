import pytest
from usa_signal_bot.portfolio_rebalance.rebalance_reporting import (
    portfolio_position_to_text, rebalance_action_to_text, rebalance_limitations_text
)
from usa_signal_bot.portfolio_rebalance.rebalance_models import (
    PortfolioPosition, RebalanceAction
)
from usa_signal_bot.core.enums import RebalanceActionType, RebalanceStatus

def test_portfolio_position_to_text():
    pos = PortfolioPosition("1", "AAPL", 10, 1000, side="LONG")
    text = portfolio_position_to_text(pos)
    assert "AAPL: 10 units @ $1000.00 (LONG)" in text

def test_rebalance_action_to_text():
    act = RebalanceAction("1", "AAPL", RebalanceActionType.INCREASE, RebalanceStatus.PROPOSED, delta_notional_usd=500)
    text = rebalance_action_to_text(act)
    assert "AAPL [INCREASE]: Delta $500.00 | Status: PROPOSED" in text

def test_rebalance_limitations_text():
    text = rebalance_limitations_text()
    assert "local metadata" in text
    assert "NOT generate or send live broker orders" in text
