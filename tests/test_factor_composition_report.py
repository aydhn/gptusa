import pytest
from usa_signal_bot.feature_engine.factor_composition.factor_composition_report import (
    build_factor_composition_context,
    build_factor_composition_full_review,
    factor_composition_limitations_text
)

def test_build_factor_composition_context():
    ctx = build_factor_composition_context()
    assert ctx.research_data_only is True
    assert ctx.produces_trade_signal is False

def test_factor_composition_limitations_text():
    text = factor_composition_limitations_text()
    assert "broker" in text.lower()
    assert "telegram real send" in text.lower()
