from usa_signal_bot.regime_classification.alignment.regime_alignment_validation import validate_no_execution_language_in_regime_alignment_text
def test_validation():
    rep = validate_no_execution_language_in_regime_alignment_text("garanti")
    assert not rep.valid
