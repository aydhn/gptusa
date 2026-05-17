
def test_diagnostic_adapter():
    from usa_signal_bot.research_workflow.diagnostics_adapter import repair_queue_from_diagnostic_review
    payload = {"failure_assessments": [{"target_name": "T1", "failure_mode": "F1", "severity": "HIGH"}]}
    items = repair_queue_from_diagnostic_review(payload)
    assert len(items) == 1
    assert items[0].target_name == "T1"
