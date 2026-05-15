from usa_signal_bot.regime_map.dispersion_proxy import dispersion_score

def test_dispersion_score_empty():
    assert dispersion_score([]) is None
