import pytest
from usa_signal_bot.attribution.trade_normalizer import (
    normalize_trade_event, normalize_backtest_trades, normalize_paper_trades,
    normalize_rebalance_actions, trade_events_to_text
)

def test_normalize_trade_event():
    payload = {
        "symbol": "AAPL",
        "gross_pnl_usd": 150.0,
        "total_cost_usd": 10.0,
        "quantity": 100,
        "strategy_name": "Trend",
        "side": "BUY",
        "metadata": {"custom": "data"}
    }
    event = normalize_trade_event(payload)

    assert event.symbol == "AAPL"
    assert event.gross_pnl_usd == 150.0
    assert event.total_cost_usd == 10.0
    assert event.net_pnl_usd == 140.0  # Fallback calculation
    assert event.quantity == 100.0
    assert event.strategy_name == "Trend"
    assert event.side == "BUY"
    assert event.metadata["custom"] == "data"
    assert "broker_order_id" not in event.__dict__ # Ensure we don't accidentally pull in broker info

def test_normalize_backtest_trades():
    result = {"trades": [{"symbol": "MSFT", "net_pnl_usd": 50}]}
    events = normalize_backtest_trades(result)
    assert len(events) == 1
    assert events[0].symbol == "MSFT"

def test_normalize_paper_trades():
    payload = {"closed_trades": [{"symbol": "GOOGL", "net_pnl_usd": -20}]}
    events = normalize_paper_trades(payload)
    assert len(events) == 1
    assert events[0].symbol == "GOOGL"

def test_normalize_rebalance_actions():
    payload = {"actions": [{"symbol": "TSLA", "action_type": "BUY"}]}
    events = normalize_rebalance_actions(payload)
    assert len(events) == 1
    assert events[0].symbol == "TSLA"
    assert events[0].rebalance_action_type == "BUY"

def test_trade_events_to_text():
    events = [normalize_trade_event({"symbol": "AAPL", "net_pnl_usd": 10})]
    text = trade_events_to_text(events)
    assert "AAPL" in text
    assert "Net PnL: $10.00" in text
