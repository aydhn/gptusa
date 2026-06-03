def test_oos_robustness_metrics():
    from usa_signal_bot.backtesting.walk_forward.oos_robustness_metrics import calculate_fold_pass_rate
    assert calculate_fold_pass_rate([]) is None
