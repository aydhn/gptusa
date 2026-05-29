from usa_signal_bot.regime_classification.alignment.compatibility_schema_validator import validate_alignment_column_names
def test_schema_validator():
    errs = validate_alignment_column_names(["buy_signal", "normal_col"])
    assert len(errs) > 0
