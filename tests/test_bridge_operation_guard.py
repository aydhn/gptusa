import pytest
from usa_signal_bot.core.enums import BridgeOperation, BridgeOperationDecision
from usa_signal_bot.core.exceptions import BridgeOperationGuardError
from usa_signal_bot.paper_quarantine.bridge_operation_guard import (
    bridge_operation_decision,
    assert_bridge_operation_allowed,
)

def test_allow():
    assert bridge_operation_decision(BridgeOperation.READ_PAPER_SNAPSHOT) == BridgeOperationDecision.ALLOW
    assert bridge_operation_decision(BridgeOperation.WRITE_QUARANTINE_OUTPUT) == BridgeOperationDecision.ALLOW

def test_deny():
    assert bridge_operation_decision(BridgeOperation.WRITE_PAPER_STATE) == BridgeOperationDecision.DENY
    assert bridge_operation_decision(BridgeOperation.SEND_PAPER_ORDER) == BridgeOperationDecision.DENY
    assert bridge_operation_decision(BridgeOperation.SEND_BROKER_ORDER) == BridgeOperationDecision.DENY
    assert bridge_operation_decision(BridgeOperation.SEND_TELEGRAM_REAL) == BridgeOperationDecision.DENY
    assert bridge_operation_decision(BridgeOperation.WRITE_PRODUCTION_CONFIG) == BridgeOperationDecision.DENY

def test_assert():
    with pytest.raises(BridgeOperationGuardError):
        assert_bridge_operation_allowed(BridgeOperation.WRITE_PAPER_STATE)
