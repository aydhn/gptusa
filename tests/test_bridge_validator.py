import pytest
from usa_signal_bot.core.enums import BridgeOperation
from usa_signal_bot.paper_quarantine.quarantine_models import SupervisedDryRunBridgePlan
from usa_signal_bot.paper_quarantine.bridge_validator import (
    validate_bridge_plan_no_mutation,
    validate_bridge_plan_operations,
)

def test_no_mutation(mocker):
    p = mocker.Mock(spec=SupervisedDryRunBridgePlan)
    p.bridge_execution_enabled = False
    p.paper_state_mutation_enabled = False
    p.paper_order_enabled = False
    p.broker_order_enabled = False
    p.telegram_real_send_enabled = False
    p.production_config_write_enabled = False

    assert not validate_bridge_plan_no_mutation(p)

    p.paper_state_mutation_enabled = True
    assert validate_bridge_plan_no_mutation(p)

def test_operations(mocker):
    p = mocker.Mock(spec=SupervisedDryRunBridgePlan)
    p.allowed_operations = [BridgeOperation.READ_PAPER_SNAPSHOT]
    assert not validate_bridge_plan_operations(p)

    p.allowed_operations = [BridgeOperation.WRITE_PAPER_STATE]
    assert validate_bridge_plan_operations(p)
