def test_walk_forward_report():
    from usa_signal_bot.backtesting.walk_forward.walk_forward_report import build_walk_forward_full_review
    rev = build_walk_forward_full_review()
    assert rev.report_type.value == "FULL_PHASE150_REVIEW"
