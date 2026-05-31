from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_schema_validator import validate_no_forbidden_research_freeze_columns

def test_validate_no_forbidden_research_freeze_columns():
    errs = validate_no_forbidden_research_freeze_columns(["date", "volatility", "macd_signal_9"])
    assert len(errs) == 0
    errs = validate_no_forbidden_research_freeze_columns(["date", "buy_signal"])
    assert len(errs) == 1
    assert "buy" in errs[0]
