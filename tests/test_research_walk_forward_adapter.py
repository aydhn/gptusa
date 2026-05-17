
def test_walk_forward_adapter():
    from usa_signal_bot.research_workflow.walk_forward_adapter import walk_forward_research_items_from_window_failures
    payload = {"strategy_id": "S1", "windows": {"W1": {"oos_failure": True}, "W2": {"oos_failure": False}}}
    items = walk_forward_research_items_from_window_failures(payload)
    assert "W1" in items
    assert "W2" not in items
    assert items["W1"][0].target_name == "S1"
