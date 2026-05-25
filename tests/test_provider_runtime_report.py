from usa_signal_bot.data_provider_runtime.provider_runtime_report import build_provider_runtime_context, build_provider_runtime_full_review

def test_provider_runtime_report():
    ctx = build_provider_runtime_context()
    assert ctx.context_id is not None

    rev = build_provider_runtime_full_review()
    assert rev.review_id is not None
