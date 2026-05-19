import pytest
from usa_signal_bot.paper_shadow.governance_adapter import (
    governance_shadow_allowed,
    governance_adapter_to_text
)

def test_shadow_governance_adapter():
    payload = {"decision": "APPROVE"}
    allowed, warns = governance_shadow_allowed(payload)
    assert allowed
    assert not warns

    text = governance_adapter_to_text(payload)
    assert "Governance Shadow Adapter Summary" in text
