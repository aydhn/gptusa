def test_degradation_diagnostics():
    from usa_signal_bot.backtesting.walk_forward.degradation_diagnostics import infer_degradation_severity
    assert infer_degradation_severity(0.5) == "NONE"
