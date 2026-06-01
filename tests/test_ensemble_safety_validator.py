import pytest
from usa_signal_bot.ml_research.ensemble_scaffolding.ensemble_safety_validator import ensemble_scaffolding_text_has_trade_or_execution_language

def test_safety_validator():
    txt = "This is a research report."
    assert not ensemble_scaffolding_text_has_trade_or_execution_language(txt)

    txt_bad = "This provides guaranteed profit."
    assert ensemble_scaffolding_text_has_trade_or_execution_language(txt_bad)
