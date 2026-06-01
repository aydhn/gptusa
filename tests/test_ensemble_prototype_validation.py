from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_prototype_validation import validate_no_execution_language_in_ensemble_prototype_text

def test_validate_no_execution_language_in_ensemble_prototype_text():
    report = validate_no_execution_language_in_ensemble_prototype_text("This model is ready to deploy")
    assert report.valid is False

    report2 = validate_no_execution_language_in_ensemble_prototype_text("This model is a research prototype")
    assert report2.valid is True
