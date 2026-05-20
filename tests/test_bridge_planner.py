import pytest
from usa_signal_bot.core.enums import BridgePlanStatus, BridgeMode
from usa_signal_bot.paper_quarantine.quarantine_models import QuarantinedPaperCandidate, ReadOnlyPromotionTicket, PaperSnapshotRef
from usa_signal_bot.paper_quarantine.bridge_planner import (
    build_supervised_dry_run_bridge_plan,
    bridge_plan_from_shadow_governance_payload,
    validate_bridge_plan_safety,
)

def test_build(mocker):
    c = mocker.Mock(spec=QuarantinedPaperCandidate)
    c.candidate_id = "c1"
    c.paper_snapshot_ref = mocker.Mock(spec=PaperSnapshotRef)
    c.paper_snapshot_ref.snapshot_ref_id = "r1"
    c.risk_flags = []
    c.policy = None

    t = mocker.Mock(spec=ReadOnlyPromotionTicket)
    t.ticket_id = "t1"

    p = build_supervised_dry_run_bridge_plan(c, t)

    assert p.bridge_execution_enabled is False
    assert p.paper_state_mutation_enabled is False
    assert p.paper_order_enabled is False
    assert p.broker_order_enabled is False
    assert p.telegram_real_send_enabled is False
    assert p.production_config_write_enabled is False

def test_build_from_payload():
    p = bridge_plan_from_shadow_governance_payload({})
    assert p.paper_state_mutation_enabled is False

def test_safety_validation(mocker):
    p = bridge_plan_from_shadow_governance_payload({})
    assert not validate_bridge_plan_safety(p)
