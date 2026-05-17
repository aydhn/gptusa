
from usa_signal_bot.research_workflow.priority_scoring import priority_score_to_repair_priority
from usa_signal_bot.core.enums import RepairPriority

def test_score_mapping():
    assert priority_score_to_repair_priority(0.9) == RepairPriority.CRITICAL
    assert priority_score_to_repair_priority(0.0) == RepairPriority.DEFERRED
