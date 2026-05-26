from usa_signal_bot.feature_engine.feature_foundation_report import build_feature_foundation_context

def test_build_feature_foundation_context():
    ctx = build_feature_foundation_context()
    assert ctx.status.value in ["VALIDATED", "FAILED"]
    assert ctx.produces_trade_signal is False
    assert ctx.activation_allowed is False
