def test_score():
    from usa_signal_bot.paper_shadow_governance.acceptance_scoring import calculate_shadow_acceptance_score
    assert calculate_shadow_acceptance_score([]) is None
