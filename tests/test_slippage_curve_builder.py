import pytest
from usa_signal_bot.transaction_costs.slippage_curve_builder import build_liquidity_adjusted_slippage_curve
from usa_signal_bot.execution.liquidity_models import LiquidityProfile
from usa_signal_bot.core.enums import LiquidityStatus

def test_liquidity_adjusted_curve():
    profile = LiquidityProfile(
        profile_id="1",
        symbol="SPY",
        created_at_utc="2024",
        status=LiquidityStatus.ILLIQUID,
        avg_daily_volume=None,
        avg_dollar_volume=None,
        median_daily_volume=None,
        median_dollar_volume=None,
        last_price=None,
        last_volume=None,
        atr_pct=None,
        gap_pct=None,
        stale_data_days=None,
        metrics=[]
    )
    curve = build_liquidity_adjusted_slippage_curve("SPY", profile)
    assert curve.liquidity_multiplier > 1.0

def test_high_atr_multiplier():
    curve = build_liquidity_adjusted_slippage_curve("SPY", None, None, 5.0)
    assert curve.volatility_multiplier > 1.0
