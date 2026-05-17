
def test_regime_adapter():
    from usa_signal_bot.research_workflow.regime_adapter import repair_items_from_regime_failures
    payload = {"regime_failures": [{"rule_name": "R1", "failure_mode": "M1"}]}
    items = repair_items_from_regime_failures(payload)
    assert len(items) == 1
    assert items[0].target_name == "R1"
