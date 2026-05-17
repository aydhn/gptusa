
def test_strategy_adaptation_adapter():
    from usa_signal_bot.research_workflow.strategy_adaptation_adapter import repair_items_from_strategy_gates
    payload = {"strategy_gate_failures": [{"target_strategy": "S2", "failure_mode": "G1"}]}
    items = repair_items_from_strategy_gates(payload)
    assert len(items) == 1
    assert items[0].target_name == "S2"
