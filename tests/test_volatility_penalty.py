import pytest
from usa_signal_bot.transaction_costs.volatility_penalty import estimate_volatility_penalty_bps, estimate_gap_penalty_bps

def test_low_volatility():
    assert estimate_volatility_penalty_bps(1.0) == 0.0

def test_high_volatility():
    assert estimate_volatility_penalty_bps(3.0) > 0.0

def test_gap_penalty():
    assert estimate_gap_penalty_bps(2.0) == 0.0
    assert estimate_gap_penalty_bps(5.0) > 0.0
