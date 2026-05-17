
from usa_signal_bot.research_workflow.workflow_validation import validate_no_live_execution_language_in_workflow

def test_workflow_validation():
    rep = validate_no_live_execution_language_in_workflow("kesin al")
    assert not rep.valid
    rep = validate_no_live_execution_language_in_workflow("safe string")
    assert rep.valid
