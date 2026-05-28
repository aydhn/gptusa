import pytest
from usa_signal_bot.feature_engine.final_closure.final_closure_report import build_final_closure_context, build_final_closure_full_review

def test_build_final_closure_context():
    # Will use the mock store read, which currently returns empty / invalid payload
    ctx = build_final_closure_context()
    assert ctx.ready_for_phase126 is False
    assert ctx.activation_allowed is False

def test_build_final_closure_full_review():
    review = build_final_closure_full_review()
    assert review.context.ready_for_phase126 is False
