import pytest
from usa_signal_bot.core.enums import BridgeOperation
from usa_signal_bot.paper_quarantine.quarantine_policy import (
    default_quarantine_policy,
    strict_quarantine_policy,
    allowed_quarantine_bridge_operations,
    denied_quarantine_bridge_operations,
    validate_quarantine_policy_safety,
    quarantine_policy_to_text,
)

def test_default_safe():
    p = default_quarantine_policy()
    assert validate_quarantine_policy_safety(p) == []

def test_strict_safe():
    p = strict_quarantine_policy()
    assert validate_quarantine_policy_safety(p) == []

def test_allowed_list():
    assert BridgeOperation.READ_PAPER_SNAPSHOT in allowed_quarantine_bridge_operations()

def test_denied_list():
    assert BridgeOperation.WRITE_PAPER_STATE in denied_quarantine_bridge_operations()

def test_to_text():
    p = default_quarantine_policy()
    assert "Manual Review Required" in quarantine_policy_to_text(p)
