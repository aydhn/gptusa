import pytest
from pathlib import Path
from usa_signal_bot.feature_engine.factor_composition.enriched_feature_table_loader import (
    load_enriched_feature_table_csv,
    validate_enriched_feature_table_input
)

def test_load_and_validate_valid_csv():
    df = load_enriched_feature_table_csv(Path('tests/fixtures/factor_composition/sample_enriched_feature_table_aapl.csv'))
    errors = validate_enriched_feature_table_input(df)
    assert len(errors) == 0

def test_load_and_validate_forbidden_columns():
    df = load_enriched_feature_table_csv(Path('tests/fixtures/factor_composition/sample_forbidden_factor_columns.csv'))
    errors = validate_enriched_feature_table_input(df)
    assert len(errors) > 0
    assert any("buy_signal" in e.lower() for e in errors)
    assert any("sell_signal" in e.lower() for e in errors)
    assert any("portfolio_weight" in e.lower() for e in errors)
