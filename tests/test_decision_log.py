
from usa_signal_bot.research_workflow.decision_log import create_decision_log_entry

def test_decision_log():
    entry = create_decision_log_entry("E1", "ID1", "D1", "R1")
    assert entry.entity_type == "E1"
