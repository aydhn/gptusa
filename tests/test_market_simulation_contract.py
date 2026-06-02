import pytest
from usa_signal_bot.backtesting.market_simulation_contract import build_market_simulation_contract
from usa_signal_bot.backtesting.backtest_dataset_contract import build_default_backtest_dataset_contract
from usa_signal_bot.backtesting.backtest_event_timeline import build_default_backtest_event_timeline
from usa_signal_bot.backtesting.execution_assumptions import build_default_execution_assumption
from usa_signal_bot.backtesting.transaction_cost_model import build_default_transaction_cost_model
from usa_signal_bot.backtesting.commission_model import build_default_commission_model
from usa_signal_bot.backtesting.spread_model import build_default_spread_model
from usa_signal_bot.backtesting.slippage_model import build_default_slippage_model
from usa_signal_bot.backtesting.liquidity_guard import build_default_liquidity_guard
from usa_signal_bot.backtesting.partial_fill_assumptions import build_default_partial_fill_assumption
from usa_signal_bot.backtesting.execution_latency_assumptions import build_default_execution_latency_assumption
from usa_signal_bot.backtesting.phase146_models import BacktestInputReference, BacktestInputKind

def test_market_simulation_contract():
    ref = BacktestInputReference(
        input_ref_id="x", created_at_utc="y", input_kind=BacktestInputKind.PRICE_BAR_DATA,
        source_artifact_name="", source_path="", source_hash="", available=True, read_only=True, required=True,
        row_count=1, columns=["symbol", "timestamp", "open", "high", "low", "close", "volume"],
        forbidden_columns_detected=[], research_data_only=True, offline_backtest_research_only=True,
        warnings=[], errors=[], risk_flags=[], metadata={}
    )
    ds = build_default_backtest_dataset_contract([ref])
    tl = build_default_backtest_event_timeline()
    ex = build_default_execution_assumption()
    tx = build_default_transaction_cost_model()
    cm = build_default_commission_model()
    sp = build_default_spread_model()
    sl = build_default_slippage_model()
    lq = build_default_liquidity_guard()
    pf = build_default_partial_fill_assumption()
    la = build_default_execution_latency_assumption()

    m = build_market_simulation_contract(ds, tl, ex, tx, cm, sp, sl, lq, pf, la)
    assert m.allows_live_execution is False
    assert m.simulation_contract_valid is True
