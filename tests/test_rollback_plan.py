
from usa_signal_bot.research_workflow.rollback_plan import build_default_rollback_plan

def test_rollback_plan():
    plan = build_default_rollback_plan()
    assert plan["requires_manual_review"] is True
