import pytest
from usa_signal_bot.paper_shadow_governance.governance_validation import (
    validate_no_live_execution_language_in_shadow_governance,
    validate_no_broker_execution_fields_in_shadow_governance
)

def test_no_live_language():
    rep = validate_no_live_execution_language_in_shadow_governance("This is live approved!")
    assert not rep.valid
    assert len(rep.issues) > 0

def test_no_broker_fields():
    rep = validate_no_broker_execution_fields_in_shadow_governance({"broker_order_id": "123"})
    assert not rep.valid
