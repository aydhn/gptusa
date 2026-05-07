import pytest
from pathlib import Path
from usa_signal_bot.paper.paper_engine import PaperTradingEngine, PaperEngineConfig
from usa_signal_bot.core.enums import PaperExecutionMode, PaperOrderSide, PaperOrderType
from usa_signal_bot.paper.paper_orders import create_paper_order_intent

def test_engine_validate_only(tmp_path):
    cfg = PaperEngineConfig(
        execution_mode=PaperExecutionMode.VALIDATE_ONLY,
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
    engine = PaperTradingEngine(tmp_path, config=cfg)

    intent = create_paper_order_intent("AAPL", "1d", PaperOrderSide.BUY, 10.0, order_type=PaperOrderType.MARKET, notional=1500.0)

    res = engine.run_order_intents([intent])

    # In validate only mode, orders are ACCEPTED but not FILLED
    assert len(res.orders) == 1
    assert res.orders[0].status.value == "ACCEPTED"
    assert len(res.fills) == 0

def test_engine_dry_run(tmp_path):
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
    engine = PaperTradingEngine(tmp_path, config=cfg)

    intent = create_paper_order_intent("AAPL", "1d", PaperOrderSide.BUY, 10.0, notional=1500.0)
    res = engine.run_order_intents([intent])

    # In dry run mode, orders are SKIPPED (no fill simulated)
    assert len(res.orders) == 1
    assert res.orders[0].status.value == "SKIPPED"
    assert len(res.fills) == 0

def test_engine_max_notional_reject(tmp_path):
    cfg = PaperEngineConfig(
        execution_mode=PaperExecutionMode.VALIDATE_ONLY,
        starting_cash=10000.0,
        fee_bps=1.0,
        slippage_bps=2.0,
        allow_fractional_quantity=True,
        allow_short=False,
        max_positions=20,
        max_order_notional=1000.0, # low limit
        max_total_exposure_pct=0.8,
        reject_duplicate_symbol_position=True,
        write_outputs=False
    )
    engine = PaperTradingEngine(tmp_path, config=cfg)

    intent = create_paper_order_intent("AAPL", "1d", PaperOrderSide.BUY, 10.0, notional=5000.0) # over limit
    res = engine.run_order_intents([intent])

    assert res.orders[0].status.value == "REJECTED"
    assert res.orders[0].reject_reason.value == "VALIDATION_FAILED"
