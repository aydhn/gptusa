import pytest
from usa_signal_bot.ml_research.ensemble_scaffolding.ensemble_scaffolding_reporting import ensemble_scaffolding_limitations_text

def test_rep():
    txt = ensemble_scaffolding_limitations_text()
    assert "No trade signals" in txt
