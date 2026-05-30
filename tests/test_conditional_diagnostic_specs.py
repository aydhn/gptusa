import pytest
from usa_signal_bot.regime_classification.validation.conditional_diagnostic_specs import build_default_conditional_diagnostic_specs

def test_build_default_conditional_diagnostic_specs():
    specs = build_default_conditional_diagnostic_specs()
    assert len(specs) == 8
