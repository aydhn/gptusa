import pytest
from usa_signal_bot.paper.paper_fills import (
    PaperFillConfig, default_paper_fill_config, validate_paper_fill_config,
    calculate_paper_fill_price, calculate_paper_fill_fees, calculate_paper_net_cash_impact,
    simulate_paper_fill, simulate_paper_fill_from_bar, paper_fill_summary
)
from usa_signal_bot.paper.paper_orders import create_paper_order_intent, create_paper_order
from usa_signal_bot.paper.virtual_account import create_virtual_account
from usa_signal_bot.core.enums import PaperOrderSide, PaperOrderType
from usa_signal_bot.data.models import OHLCVBar

def test_paper_fill_config():
    cfg = default_paper_fill_config()
    assert cfg.fee_bps == 1.0
    assert cfg.slippage_bps == 2.0

    validate_paper_fill_config(cfg)

    with pytest.raises(ValueError):
        validate_paper_fill_config(PaperFillConfig(-1.0, 2.0, False))

def test_calculate_fill_price():
    # BUY goes up (against us)
    p1 = calculate_paper_fill_price(PaperOrderSide.BUY, 100.0, 100.0) # 100 bps = 1%
    assert p1 == 101.0

    # SELL goes down (against us)
    p2 = calculate_paper_fill_price(PaperOrderSide.SELL, 100.0, 100.0) # 1%
    assert p2 == 99.0

def test_calculate_fees():
    f = calculate_paper_fill_fees(10000.0, 10.0) # 10 bps = 0.1%
    assert f == 10.0

def test_calculate_net_cash_impact():
    # Buy 100 shares @ $10 = $1000 notional, plus $1 fee
    i1 = calculate_paper_net_cash_impact(PaperOrderSide.BUY, 1000.0, 1.0)
    assert i1 == -1001.0

    # Sell 100 shares @ $10 = $1000 notional, minus $1 fee
    i2 = calculate_paper_net_cash_impact(PaperOrderSide.SELL, 1000.0, 1.0)
    assert i2 == 999.0

def test_simulate_paper_fill():
    acct = create_virtual_account("test")
    intent = create_paper_order_intent("AAPL", "1d", PaperOrderSide.BUY, 10.0)
    order = create_paper_order(acct, intent)

    cfg = PaperFillConfig(fee_bps=10.0, slippage_bps=100.0, allow_partial_fills=False)
    fill = simulate_paper_fill(order, 100.0, cfg)

    assert fill.fill_price == 101.0 # 100 * 1.01
    assert fill.gross_notional == 1010.0 # 10 * 101
    assert fill.fees == 1.01 # 1010 * 0.001
    assert fill.net_cash_impact == -1011.01

def test_simulate_paper_fill_from_bar():
    acct = create_virtual_account("test")
    intent = create_paper_order_intent("AAPL", "1d", PaperOrderSide.BUY, 10.0, order_type=PaperOrderType.NEXT_OPEN)
    order = create_paper_order(acct, intent)

    bar = OHLCVBar(symbol='AAPL', timeframe='1d', timestamp_utc='2026-05-06T00:00:00Z', open=100.0, high=110.0, low=90.0, close=105.0, volume=10000)

    cfg = PaperFillConfig(fee_bps=0.0, slippage_bps=0.0, allow_partial_fills=False)
    fill = simulate_paper_fill_from_bar(order, bar, cfg)

    assert fill.fill_price == 100.0
