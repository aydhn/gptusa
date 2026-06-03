def test_walk_forward_safety():
    from usa_signal_bot.backtesting.walk_forward.walk_forward_safety_validator import walk_forward_text_has_trade_or_execution_language
    assert walk_forward_text_has_trade_or_execution_language("this is investment advice")
