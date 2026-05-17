
def test_backtest_adapter():
    from usa_signal_bot.research_workflow.backtest_adapter import backtest_research_items_from_failures
    payload = {"failures": [{"name": "B1", "reason": "R1"}]}
    items = backtest_research_items_from_failures(payload)
    assert len(items) == 1
    assert items[0].target_name == "B1"
