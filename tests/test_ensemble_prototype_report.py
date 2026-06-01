from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_prototype_report import build_ensemble_prototype_full_review

def test_build_ensemble_prototype_full_review():
    review = build_ensemble_prototype_full_review()
    assert review.readiness_gate.ready_for_phase144 is True
    assert review.context.offline_ml_research_only is True
