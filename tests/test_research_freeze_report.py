from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_report import build_regime_research_freeze_full_review

def test_build_regime_research_freeze_full_review():
    review = build_regime_research_freeze_full_review()
    assert review.review_id is not None
    assert review.context is not None
