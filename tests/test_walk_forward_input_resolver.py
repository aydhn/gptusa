def test_input_resolver():
    from usa_signal_bot.backtesting.walk_forward.walk_forward_input_resolver import detect_forbidden_walk_forward_columns
    assert "broker_order" in detect_forbidden_walk_forward_columns(["broker_order", "safe_col"])
