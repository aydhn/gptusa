
def test_rebalance_adapter():
    from usa_signal_bot.research_workflow.rebalance_adapter import repair_items_from_rebalance_failures
    payload = {"rebalance_failures": [{"rule_name": "RB1", "failure_mode": "M1"}]}
    items = repair_items_from_rebalance_failures(payload)
    assert len(items) == 1
    assert items[0].target_name == "RB1"
