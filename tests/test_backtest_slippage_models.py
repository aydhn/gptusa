import pytest
from usa_signal_bot.backtesting.slippage_models import (
    SlippageConfig, SlippageModelType, calculate_slippage,
    default_slippage_config, slippage_breakdown_to_dict
)
from usa_signal_bot.core.enums import BacktestOrderSide, LiquidityBucket
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.core.exceptions import SlippageModelError

@pytest.fixture
def bar():
    return OHLCVBar(symbol="AAPL", timestamp_utc="2024-01-01T00:00:00Z", timeframe="1d", open=100.0, high=102.0, low=98.0, close=101.0, volume=10000)

def test_default_slippage_config():
    config = default_slippage_config()
    assert config.model_type == SlippageModelType.FIXED_BPS
    assert config.fixed_bps == 2.0

def test_fixed_bps_buy(bar):
    config = SlippageConfig(model_type=SlippageModelType.FIXED_BPS, fixed_bps=100.0) # 1%
    res = calculate_slippage(100.0, 10.0, BacktestOrderSide.BUY, bar, config)
    assert res.adjusted_price == 101.0 # 100 + 1%

def test_fixed_bps_sell(bar):
    config = SlippageConfig(model_type=SlippageModelType.FIXED_BPS, fixed_bps=100.0) # 1%
    res = calculate_slippage(100.0, 10.0, BacktestOrderSide.SELL, bar, config)
    assert res.adjusted_price == 99.0 # 100 - 1%

def test_spread_proxy(bar):
    config = SlippageConfig(model_type=SlippageModelType.SPREAD_PROXY, spread_bps=20.0)
    res = calculate_slippage(100.0, 10.0, BacktestOrderSide.BUY, bar, config)
    assert res.slippage_bps == 10.0 # Half of spread
    assert res.adjusted_price == 100.1

def test_volume_participation(bar):
    config = SlippageConfig(model_type=SlippageModelType.VOLUME_PARTICIPATION, volume_participation_rate=0.01)
    res = calculate_slippage(100.0, 50.0, BacktestOrderSide.BUY, bar, config) # 50/10000 = 0.005 < 0.01
    assert res.slippage_bps == 1.0 # base slippage

def test_volume_participation_high_volume(bar):
    config = SlippageConfig(model_type=SlippageModelType.VOLUME_PARTICIPATION, volume_participation_rate=0.01, volume_impact_factor=10.0)
    res = calculate_slippage(100.0, 200.0, BacktestOrderSide.BUY, bar, config) # 200/10000 = 0.02 > 0.01
    # excess = 0.01, penalty = 0.01 * 10 * 10000 = 1000, slippage_bps = 1 + 1000 = 1001, capped at 100 max
    assert res.slippage_bps == 100.0 # hit max

def test_volatility_adjusted(bar):
    config = SlippageConfig(model_type=SlippageModelType.VOLATILITY_ADJUSTED, volatility_multiplier=1.0)
    res = calculate_slippage(100.0, 10.0, BacktestOrderSide.BUY, bar, config)
    # vol proxy = (102-98)/98 = 4/98 = 0.0408
    # slippage = 2.0 + 0.0408 * 10000 = 410 bps
    # capped at 100
    assert res.slippage_bps == 100.0

def test_cap_slippage_bps(bar):
    config = SlippageConfig(model_type=SlippageModelType.FIXED_BPS, fixed_bps=200.0, max_slippage_bps=50.0)
    res = calculate_slippage(100.0, 10.0, BacktestOrderSide.BUY, bar, config)
    assert res.slippage_bps == 50.0

def test_liquidity_bucket(bar):
    config = default_slippage_config()
    res = calculate_slippage(100.0, 10.0, BacktestOrderSide.BUY, bar, config)
    assert res.liquidity_bucket == LiquidityBucket.NORMAL # 101 * 10000 = 1,010,000

def test_breakdown_to_dict(bar):
    config = default_slippage_config()
    res = calculate_slippage(100.0, 10.0, BacktestOrderSide.BUY, bar, config)
    d = slippage_breakdown_to_dict(res)
    assert d['adjusted_price'] == 100.02
