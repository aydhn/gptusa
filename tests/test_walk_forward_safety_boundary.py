def test_walk_forward_safety_boundary():
    from usa_signal_bot.backtesting.walk_forward.walk_forward_safety_boundary import build_walk_forward_safety_boundary_rules
    rules = build_walk_forward_safety_boundary_rules()
    assert len(rules) > 0
