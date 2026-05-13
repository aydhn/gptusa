import pytest
import datetime
from usa_signal_bot.core.enums import LiquidityMetricName, LiquidityStatus
from usa_signal_bot.core.exceptions import ExecutionValidationError
from usa_signal_bot.execution.liquidity_models import (
    LiquidityMetric,
    LiquidityProfile,
    create_liquidity_metric_id,
    create_liquidity_profile_id,
    validate_liquidity_metric,
    validate_liquidity_profile,
    liquidity_metric_to_dict,
    liquidity_profile_to_dict
)

def test_liquidity_metric():
    m = LiquidityMetric(
        metric_id=create_liquidity_metric_id("SPY", LiquidityMetricName.AVG_DAILY_VOLUME),
        symbol="SPY",
        metric_name=LiquidityMetricName.AVG_DAILY_VOLUME,
        value=1000.0,
        unit="shares",
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        lookback_bars=60
    )
    validate_liquidity_metric(m)
    d = liquidity_metric_to_dict(m)
    assert d["symbol"] == "SPY"
    assert d["value"] == 1000.0

def test_liquidity_profile():
    p = LiquidityProfile(
        profile_id=create_liquidity_profile_id("SPY"),
        symbol="SPY",
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        status=LiquidityStatus.EXCELLENT,
        avg_daily_volume=1000000.0,
        avg_dollar_volume=100000000.0,
        median_daily_volume=1000000.0,
        median_dollar_volume=100000000.0,
        last_price=100.0,
        last_volume=1000000.0,
        atr_pct=1.5,
        gap_pct=0.1,
        stale_data_days=0,
        metrics=[]
    )
    validate_liquidity_profile(p)
    d = liquidity_profile_to_dict(p)
    assert d["symbol"] == "SPY"

def test_invalid_profile():
    p = LiquidityProfile(
        profile_id="123",
        symbol="SPY",
        created_at_utc="",
        status=LiquidityStatus.EXCELLENT,
        avg_daily_volume=-100.0,
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
    with pytest.raises(ExecutionValidationError):
        validate_liquidity_profile(p)
