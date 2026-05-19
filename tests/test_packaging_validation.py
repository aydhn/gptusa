from usa_signal_bot.release_packaging.packaging_validation import validate_no_live_execution_language_in_bundle

def test_packaging_validation():
    rep = validate_no_live_execution_language_in_bundle("live approved")
    assert rep.valid is False
