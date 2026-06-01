from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_prototype_schema_validator import validate_no_forbidden_ensemble_evaluation_columns

def test_validate_no_forbidden_ensemble_evaluation_columns():
    errors = validate_no_forbidden_ensemble_evaluation_columns(["buy_signal", "research_score"])
    assert len(errors) == 2 # 'signal' and 'buy'

    errors2 = validate_no_forbidden_ensemble_evaluation_columns(["research_ensemble_score", "timestamp"])
    assert len(errors2) == 0
