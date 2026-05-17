
def test_allocation_adapter():
    from usa_signal_bot.research_workflow.allocation_adapter import repair_items_from_allocation_failures
    payload = {"sizing_failures": [{"rule_name": "A1", "failure_mode": "M1"}]}
    items = repair_items_from_allocation_failures(payload)
    assert len(items) == 1
    assert items[0].target_name == "A1"
