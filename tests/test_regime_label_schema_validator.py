import pandas as pd
from usa_signal_bot.regime_classification.labeling.regime_label_schema_validator import validate_regime_label_result_columns

def test_schema_validator():
    bad_columns = ["symbol", "timestamp", "buy_signal", "regime_label_research"]
    errors = validate_regime_label_result_columns(bad_columns)
    assert len(errors) > 0
    assert any("buy" in e.lower() for e in errors)

    good_columns = ["symbol", "timestamp", "regime_label_research", "regime_label_confidence"]
    errors = validate_regime_label_result_columns(good_columns)
    assert len(errors) == 0
