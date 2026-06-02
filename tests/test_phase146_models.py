import pytest
from usa_signal_bot.backtesting.phase146_models import (
    create_advanced_ml_closure_ingestion_id,
    create_backtest_input_reference_id,
    create_backtest_dataset_contract_id
)

def test_id_generation():
    assert "ingest_" in create_advanced_ml_closure_ingestion_id()
    assert "input_" in create_backtest_input_reference_id()
    assert "dscontract_" in create_backtest_dataset_contract_id()
