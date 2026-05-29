from usa_signal_bot.regime_classification.alignment.alignment_diagnostics_builder import build_alignment_diagnostics_profiles
def test_diagnostics():
    res = build_alignment_diagnostics_profiles([])
    assert len(res) == 0
