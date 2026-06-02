import pytest
from usa_signal_bot.backtesting.backtest_dataset_contract import build_default_backtest_dataset_contract
from usa_signal_bot.backtesting.phase146_models import BacktestInputReference, BacktestInputKind

def test_build_dataset_contract():
    ref = BacktestInputReference(
        input_ref_id="x", created_at_utc="y", input_kind=BacktestInputKind.PRICE_BAR_DATA,
        source_artifact_name="", source_path="", source_hash="", available=True, read_only=True, required=True,
        row_count=1, columns=["symbol", "timestamp", "open", "high", "low", "close", "volume"],
        forbidden_columns_detected=[], research_data_only=True, offline_backtest_research_only=True,
        warnings=[], errors=[], risk_flags=[], metadata={}
    )
    c = build_default_backtest_dataset_contract([ref])
    assert c.contract_valid is True
