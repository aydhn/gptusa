import pytest
from usa_signal_bot.paper.paper_reporting import (
    paper_engine_config_to_text, virtual_account_report_to_text,
    paper_order_intent_to_text, paper_limitations_text
)
from usa_signal_bot.paper.paper_engine import PaperEngineConfig
from usa_signal_bot.paper.virtual_account import create_virtual_account
from usa_signal_bot.paper.paper_orders import create_paper_order_intent
from usa_signal_bot.core.enums import PaperExecutionMode, PaperOrderSide

def test_paper_engine_config_to_text():
    cfg = PaperEngineConfig(
        execution_mode=PaperExecutionMode.DRY_RUN,
        starting_cash=10000.0,
        fee_bps=1.0,
        slippage_bps=2.0,
        allow_fractional_quantity=True,
        allow_short=False,
        max_positions=20,
        max_order_notional=10000.0,
        max_total_exposure_pct=0.8,
        reject_duplicate_symbol_position=True,
        write_outputs=False
    )

    txt = paper_engine_config_to_text(cfg)
    assert "PAPER ENGINE CONFIG" in txt
    assert "DRY_RUN" in txt

def test_virtual_account_report_to_text():
    acct = create_virtual_account("test_name", 1000.0)
    txt = virtual_account_report_to_text(acct)
    assert "test_name" in txt
    assert "1,000.00" in txt

def test_paper_order_intent_to_text():
    intent = create_paper_order_intent("AAPL", "1d", PaperOrderSide.BUY, 10.0)
    txt = paper_order_intent_to_text(intent)
    assert "BUY AAPL" in txt
    assert "10.0" in txt

def test_paper_limitations_text():
    txt = paper_limitations_text()
    assert "NO BROKER ORDERS" in txt
    assert "NOT constitute investment advice" in txt
