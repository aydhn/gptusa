import pytest
from usa_signal_bot.feature_engine.factor_explainability.explainability_report import build_explainability_context, build_explainability_full_review

def test_build_explainability_context():
    ctx = build_explainability_context()
    assert ctx.ready_for_phase124 is True
    assert ctx.activation_allowed is False

def test_build_explainability_full_review():
    rev = build_explainability_full_review()
    assert rev.context.status.value == "CREATED"
