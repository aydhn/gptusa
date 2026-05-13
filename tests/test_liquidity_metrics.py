import pytest
from usa_signal_bot.core.enums import LiquidityStatus
from usa_signal_bot.execution.liquidity_metrics import (
    calculate_avg_daily_volume,
    calculate_avg_dollar_volume,
    calculate_atr_pct,
    calculate_liquidity_profile,
    liquidity_profile_to_text
)

def test_liquidity_metrics():
    rows = [
        {"date": "2023-01-01", "open": 100, "high": 105, "low": 95, "close": 102, "volume": 1000000},
        {"date": "2023-01-02", "open": 102, "high": 104, "low": 98, "close": 100, "volume": 2000000},
    ]

    adv = calculate_avg_daily_volume(rows, 60)
    assert adv == 1500000.0

    addv = calculate_avg_dollar_volume(rows, 60)
    assert addv == (102*1000000 + 100*2000000) / 2

    atr = calculate_atr_pct(rows, 14)
    # Only 2 rows so ATR might not be fully accurate, but should compute or None
    assert atr is None

def test_liquidity_profile_calc():
    rows = [{"date": "2023-01-01", "open": 100, "high": 105, "low": 95, "close": 102, "volume": 1000000}] * 60
    profile = calculate_liquidity_profile("SPY", rows)
    assert profile.status == LiquidityStatus.GOOD

    txt = liquidity_profile_to_text(profile)
    assert "SPY" in txt
