import pytest
from usa_signal_bot.core.enums import SignalAction, PositionSizingMethod
from usa_signal_bot.risk.risk_models import PositionSizingRequest
from usa_signal_bot.risk.position_sizing import (
    default_position_sizing_config,
    calculate_position_size
)

@pytest.fixture
def base_request():
    return PositionSizingRequest(
        candidate_id="cand1", symbol="AAPL", strategy_name="strat1", timeframe="1d",
        action=SignalAction.LONG, confidence=0.8, rank_score=80.0, price=100.0,
        portfolio_equity=100000.0, available_cash=100000.0,
        volatility_value=0.02, atr_value=2.0
    )

def test_fixed_notional(base_request):
    cfg = default_position_sizing_config()
    cfg.method = PositionSizingMethod.FIXED_NOTIONAL
    cfg.fixed_notional = 5000.0

    res = calculate_position_size(base_request, cfg)
    assert res.approved_notional == 5000.0
    assert res.approved_quantity == 50.0

def test_fixed_fractional(base_request):
    cfg = default_position_sizing_config()
    cfg.method = PositionSizingMethod.FIXED_FRACTIONAL
    cfg.fixed_fraction_pct = 0.1 # 10k

    res = calculate_position_size(base_request, cfg)
    assert res.approved_notional == 10000.0
    assert res.approved_quantity == 100.0

def test_volatility_adjusted(base_request):
    cfg = default_position_sizing_config()
    cfg.method = PositionSizingMethod.VOLATILITY_ADJUSTED
    cfg.volatility_target_pct = 0.01 # Target is half of actual 0.02, so size should halve

    res = calculate_position_size(base_request, cfg)
    assert res.approved_notional == 10000.0
    assert res.capped == True

def test_atr_risk(base_request):
    cfg = default_position_sizing_config()
    cfg.method = PositionSizingMethod.ATR_RISK
    cfg.risk_per_trade_pct = 0.01 # $1000 risk
    cfg.atr_multiplier = 2.0 # risk per share = 4.0

    res = calculate_position_size(base_request, cfg)
    assert res.approved_notional == 10000.0
    assert res.capped == True

    cfg.max_notional = 50000.0
    res2 = calculate_position_size(base_request, cfg)
    assert res2.approved_notional == 25000.0
    assert res2.approved_quantity == 250.0

def test_apply_size_caps(base_request):
    cfg = default_position_sizing_config()
    cfg.max_notional = 2000.0
    res = calculate_position_size(base_request, cfg)
    assert res.approved_notional == 2000.0
    assert res.capped == True
