import pytest
from usa_signal_bot.feature_engine.factor_explainability.research_report_sections import build_limitations_section

def test_build_limitations_section():
    sec = build_limitations_section()
    assert sec.title == "Limitations"
    assert "not use for live trading" in sec.body
