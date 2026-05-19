import pytest
from usa_signal_bot.core.enums import SandboxActivationStatus, SandboxRuntimeMode, SandboxOperation
from usa_signal_bot.release_sandbox.sandbox_models import SandboxActivationPlan
from usa_signal_bot.release_sandbox.runtime_context import (
    build_sandbox_runtime_context, validate_runtime_context_safety, runtime_context_to_text
)

def test_build_sandbox_runtime_context():
    plan = SandboxActivationPlan(
        activation_id="a1", created_at_utc="now", bundle_id="b1", bundle_version="v1",
        status=SandboxActivationStatus.VALIDATED, mount_plan=None, bundle_validation_summary={},
        compatibility_summary={}, safety_summary={}, runtime_mode=SandboxRuntimeMode.FULL_SAFE_PREVIEW,
        manual_review_required=False, allowed_for_production_apply=False, allowed_for_order_routing=False,
        allowed_for_paper_state_mutation=False, warnings=[], errors=[]
    )
    bundle = {"overlay": {"key": "val"}, "artifacts": [{"name": "art1"}]}

    ctx = build_sandbox_runtime_context(plan, bundle)

    assert ctx.bundle_id == "b1"
    assert ctx.in_memory_config["key"] == "val"
    assert len(ctx.mounted_artifacts) == 1
    assert ctx.allowed_to_send_orders is False
    assert ctx.allowed_to_mutate_paper_state is False

def test_validate_runtime_context_safety():
    plan = SandboxActivationPlan(
        activation_id="a1", created_at_utc="now", bundle_id="b1", bundle_version="v1",
        status=SandboxActivationStatus.VALIDATED, mount_plan=None, bundle_validation_summary={},
        compatibility_summary={}, safety_summary={}, runtime_mode=SandboxRuntimeMode.FULL_SAFE_PREVIEW,
        manual_review_required=False, allowed_for_production_apply=False, allowed_for_order_routing=False,
        allowed_for_paper_state_mutation=False, warnings=[], errors=[]
    )
    bundle = {}
    ctx = build_sandbox_runtime_context(plan, bundle)

    warns = validate_runtime_context_safety(ctx)
    assert not warns

    ctx.allowed_to_send_orders = True
    warns = validate_runtime_context_safety(ctx)
    assert len(warns) == 1
    assert "sending orders" in warns[0].lower()
