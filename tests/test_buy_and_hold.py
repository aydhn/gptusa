import pytest
from usa_signal_bot.backtesting.buy_and_hold import (
    BuyAndHoldConfig, BuyAndHoldResult, default_buy_and_hold_config,
    validate_buy_and_hold_config, build_cash_baseline, run_buy_and_hold_baseline,
    buy_and_hold_result_to_dict, buy_and_hold_result_to_text
)
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.backtesting.benchmark_models import BenchmarkSpec
from usa_signal_bot.core.enums import BenchmarkType

def test_default_config():
    cfg = default_buy_and_hold_config()
    assert cfg.symbol == "SPY"
    assert cfg.starting_cash == 100000.0

def test_validate_config():
    cfg = default_buy_and_hold_config()
    validate_buy_and_hold_config(cfg)

    cfg.starting_cash = 0
    with pytest.raises(ValueError):
        validate_buy_and_hold_config(cfg)

def test_build_cash_baseline():
    ts = ["2024-01-01T00:00:00Z", "2024-01-02T00:00:00Z"]
    cash_bl = build_cash_baseline(10000.0, ts)
    assert len(cash_bl.points) == 2
    assert cash_bl.ending_equity == 10000.0
    assert cash_bl.total_return_pct == 0.0

def test_run_buy_and_hold_baseline():
    cfg = default_buy_and_hold_config(starting_cash=1000.0)
    bars = [
        OHLCVBar(symbol="SPY", timestamp_utc="2024-01-01T00:00:00Z", timeframe="1d", open=100.0, high=110.0, low=90.0, close=105.0, volume=1000),
        OHLCVBar(symbol="SPY", timestamp_utc="2024-01-02T00:00:00Z", timeframe="1d", open=105.0, high=120.0, low=100.0, close=110.0, volume=1000)
    ]

    res = run_buy_and_hold_baseline(bars, cfg)

    # 1000 / 100 (entry price) = 10 quantity
    assert res.quantity == 10.0
    assert res.entry_price == 100.0
    assert res.exit_price == 110.0

    # Ending equity: 10 * 110 = 1100
    assert res.ending_equity == 1100.0
    assert res.total_return == 100.0
    assert res.total_return_pct == 10.0

    d = buy_and_hold_result_to_dict(res)
    assert d["quantity"] == 10.0

    txt = buy_and_hold_result_to_text(res)
    assert "10.0" in txt

def test_run_buy_and_hold_baseline_empty():
    cfg = default_buy_and_hold_config()
    res = run_buy_and_hold_baseline([], cfg)
    assert res.ending_equity is None
    assert "No bars provided" in res.errors
