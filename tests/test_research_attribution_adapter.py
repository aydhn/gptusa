
def test_attribution_adapter():
    from usa_signal_bot.research_workflow.attribution_adapter import repair_items_from_negative_attribution
    payload = {"negative_contributors": [{"name": "N1"}]}
    items = repair_items_from_negative_attribution(payload)
    assert len(items) == 1
    assert items[0].target_name == "N1"
