import pytest
from usa_signal_bot.transaction_costs.participation_cost import estimate_participation_cost_bps, estimate_participation_cost_usd

def test_participation_cost():
    bps = estimate_participation_cost_bps(1.0)
    assert bps > 0.0
    usd = estimate_participation_cost_usd(bps, 1000)
    assert usd > 0.0
