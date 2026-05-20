import pytest
from usa_signal_bot.paper_dry_run_bridge.bridge_plan_ingestion import (
    ingest_bridge_plan_payload,
    extract_bridge_plan_id,
    extract_bridge_plan_status,
    bridge_plan_supports_session,
    bridge_plan_safety_checks,
    bridge_plan_ingestion_to_text
)
from usa_signal_bot.core.enums import BridgePlanStatus

def test_bridge_plan_ingestion():
    payload = {
        "bridge_plan_id": "plan_123",
        "status": BridgePlanStatus.VALIDATED.value,
        "execution_enabled": False,
        "paper_write_enabled": False,
        "broker_write_enabled": False,
        "telegram_write_enabled": False,
        "config_write_enabled": False,
        "allowed_operations": ["read_paper_snapshot", "write_quarantine_output"]
    }

    assert extract_bridge_plan_id(payload) == "plan_123"
    assert extract_bridge_plan_status(payload) == BridgePlanStatus.VALIDATED.value

    supports, _ = bridge_plan_supports_session(payload)
    assert supports is True

    assert len(bridge_plan_safety_checks(payload)) == 0

    payload_invalid = payload.copy()
    payload_invalid["execution_enabled"] = True
    assert len(bridge_plan_safety_checks(payload_invalid)) > 0

    payload_invalid2 = payload.copy()
    payload_invalid2["allowed_operations"] = ["send_broker_order"]
    assert len(bridge_plan_safety_checks(payload_invalid2)) > 0

    assert "plan_123" in bridge_plan_ingestion_to_text(payload)
