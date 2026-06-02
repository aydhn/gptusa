import pytest
from usa_signal_bot.backtesting.liquidity_guard import build_default_liquidity_guard, evaluate_liquidity_row

def test_liquidity_guard():
    g = build_default_liquidity_guard()
    assert g.guard_valid is True

    # 20k volume * 10 price = 200,000 < 1,000,000 min dollar vol
    res = evaluate_liquidity_row({"close": 10.0, "volume": 20000}, g)
    assert res["passed"] is False
    assert "MIN_DOLLAR_VOLUME_FAILED" in res["reasons"]
