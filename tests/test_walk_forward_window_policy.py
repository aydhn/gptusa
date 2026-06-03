def test_window_policy():
    from usa_signal_bot.backtesting.walk_forward.walk_forward_window_policy import build_default_walk_forward_window_policy
    pol = build_default_walk_forward_window_policy()
    assert pol.policy_valid
