import pytest
from usa_signal_bot.release.advanced_acceptance_report import build_advanced_acceptance_context, build_advanced_acceptance_full_review, advanced_acceptance_limitations_text

def test_advanced_acceptance_report():
    context = build_advanced_acceptance_context()
    assert context.advanced_acceptance_only == True
    assert context.investment_advice == False

    review = build_advanced_acceptance_full_review(context)
    assert review.review_id.startswith("rev_159_")

    text = advanced_acceptance_limitations_text()
    assert "It does NOT represent a deployment approval" in text
