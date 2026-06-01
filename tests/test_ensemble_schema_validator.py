import pytest
from usa_signal_bot.ml_research.ensemble_scaffolding.ensemble_schema_validator import validate_ensemble_scaffolding_column_names

def test_schema_validator():
    cols = ["date", "macd_signal_9"]
    errs = validate_ensemble_scaffolding_column_names(cols)
    assert len(errs) == 0

    cols_bad = ["date", "buy_signal"]
    errs_bad = validate_ensemble_scaffolding_column_names(cols_bad)
    assert len(errs_bad) > 0
