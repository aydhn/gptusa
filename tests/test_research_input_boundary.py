import pytest
from usa_signal_bot.backtesting.research_input_boundary import build_backtest_research_input_contract

def test_build_research_input_boundary():
    c = build_backtest_research_input_contract()
    assert c.signal_activation_allowed is False
    assert c.order_decision_allowed is False
