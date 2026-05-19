import pytest
from usa_signal_bot.core.enums import SandboxActivationStatus, SandboxSafetyFlag
from usa_signal_bot.release_sandbox.activation_planner import (
    build_sandbox_activation_plan, activation_allowed, activation_block_reasons, activation_plan_to_text
)

def test_activation_planner():
    bundle_data = {"manifest": {"bundle_id": "b1"}}
    plan = build_sandbox_activation_plan(bundle_data)

    assert plan.status == SandboxActivationStatus.VALIDATED
    assert activation_allowed(plan) is True
    assert not activation_block_reasons(plan)

    # Introduce failure
    plan.status = SandboxActivationStatus.BLOCKED
    assert activation_allowed(plan) is False
    assert "Status is BLOCKED." in activation_block_reasons(plan)

    plan.allowed_for_production_apply = True
    assert "Unsafe flags are set to True." in activation_block_reasons(plan)

    txt = activation_plan_to_text(plan)
    assert "BLOCKED" in txt
