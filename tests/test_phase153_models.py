import pytest
from usa_signal_bot.portfolio.foundation.phase153_models import (
    BacktestClosureIngestionResult, PortfolioInputReference,
    validate_backtest_closure_ingestion_result
)

def test_backtest_closure_ingestion_model():
    res = BacktestClosureIngestionResult()
    res.ready_for_phase153 = True
    assert res.ready_for_phase153 is True

    errors = validate_backtest_closure_ingestion_result(res)
    assert len(errors) == 0

    res.live_trading_enabled = True
    errors = validate_backtest_closure_ingestion_result(res)
    assert len(errors) > 0
