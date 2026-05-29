from usa_signal_bot.regime_classification.alignment.regime_alignment_report import build_regime_alignment_context, build_regime_alignment_full_review
def test_report():
    ctx = build_regime_alignment_context()
    rev = build_regime_alignment_full_review(ctx)
    assert rev.context == ctx
