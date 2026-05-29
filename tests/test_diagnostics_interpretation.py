from usa_signal_bot.feature_engine.factor_explainability.diagnostics_interpretation import interpret_factor_diagnostics_profile

def test_interpret_factor_diagnostics_profile():
    res = interpret_factor_diagnostics_profile({})
    assert "research" in res.lower()
