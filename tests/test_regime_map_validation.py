from usa_signal_bot.regime_map.regime_map_validation import validate_no_live_execution_language_in_regime_map

def test_live_language_check():
    text = "this is a kesin kâr strategy"
    r = validate_no_live_execution_language_in_regime_map(text)
    assert r.valid == False
    assert r.error_count > 0
