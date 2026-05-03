import pytest
from usa_signal_bot.core.enums import BacktestOrderSide, BacktestOrderType, SignalAction
from usa_signal_bot.core.exceptions import BacktestOrderError
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.backtesting.order_models import (
    BacktestOrderIntent, create_order_intent_from_signal, validate_order_intent,
    is_trade_order, order_intent_to_dict
)

def test_order_intent_valid():
    order = BacktestOrderIntent("id1", "sig1", "AAPL", "1d", "2023-01-01T00:00:00Z", BacktestOrderSide.BUY, BacktestOrderType.NEXT_OPEN, 10, "test")
    validate_order_intent(order)

def test_order_intent_invalid_quantity():
    order = BacktestOrderIntent("id1", "sig1", "AAPL", "1d", "2023-01-01T00:00:00Z", BacktestOrderSide.BUY, BacktestOrderType.NEXT_OPEN, 0, "test")
    with pytest.raises(BacktestOrderError):
        validate_order_intent(order)

def test_hold_quantity_zero():
    order = BacktestOrderIntent("id1", "sig1", "AAPL", "1d", "2023-01-01T00:00:00Z", BacktestOrderSide.HOLD, BacktestOrderType.NEXT_OPEN, 0, "test")
    validate_order_intent(order) # Should pass

def test_create_order_intent_from_signal():
    sig = StrategySignal(signal_id="sig1", strategy_name="strat1", confidence_bucket=__import__('usa_signal_bot.core.enums', fromlist=['SignalConfidenceBucket']).SignalConfidenceBucket.MODERATE, reasons=[], symbol="AAPL", timeframe="1d", timestamp_utc="2023", action=SignalAction.LONG, confidence=1.0, score=100.0, feature_snapshot={}, risk_flags=[])
    order = create_order_intent_from_signal(sig, 10)
    assert order.side == BacktestOrderSide.BUY
    assert order.quantity == 10

def test_is_trade_order():
    o1 = BacktestOrderIntent("id1", "sig1", "AAPL", "1d", "2023", BacktestOrderSide.BUY, BacktestOrderType.NEXT_OPEN, 10, "")
    o2 = BacktestOrderIntent("id2", "sig1", "AAPL", "1d", "2023", BacktestOrderSide.HOLD, BacktestOrderType.NEXT_OPEN, 10, "")
    assert is_trade_order(o1) == True
    assert is_trade_order(o2) == False

def test_order_intent_to_dict():
    order = BacktestOrderIntent("id1", "sig1", "AAPL", "1d", "2023", BacktestOrderSide.BUY, BacktestOrderType.NEXT_OPEN, 10, "")
    d = order_intent_to_dict(order)
    assert d["side"] == "BUY"
