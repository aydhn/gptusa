import pytest
from usa_signal_bot.regime_classification.validation.cross_symbol_validation_profiles import build_cross_symbol_validation_profile

def test_build_cross_symbol_validation_profile():
    comp_res = []
    diagnostics = []
    p = build_cross_symbol_validation_profile(comp_res, diagnostics)
    assert p is not None
