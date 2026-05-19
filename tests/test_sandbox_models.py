import pytest
from usa_signal_bot.core.enums import SandboxOperation, SandboxMountMode, SandboxRuntimeMode, SandboxStatus, SandboxActivationStatus
from usa_signal_bot.core.exceptions import ReleaseSandboxValidationError
from usa_signal_bot.release_sandbox.sandbox_models import (
    SandboxMountPlan, SandboxActivationPlan, SandboxRuntimeContext,
    validate_sandbox_activation_plan, validate_sandbox_runtime_context,
    create_sandbox_mount_plan_id
)

def test_sandbox_mount_plan_id():
    m_id = create_sandbox_mount_plan_id()
    assert m_id.startswith("sandbox_mount_")

def test_sandbox_activation_plan_validation():
    plan = SandboxActivationPlan(
        activation_id="a1", created_at_utc="now", bundle_id="b1", bundle_version="v1",
        status=SandboxActivationStatus.PLANNED, mount_plan=None, bundle_validation_summary={},
        compatibility_summary={}, safety_summary={}, runtime_mode=SandboxRuntimeMode.DRY_RUN_PREVIEW,
        manual_review_required=False, allowed_for_production_apply=True, allowed_for_order_routing=False,
        allowed_for_paper_state_mutation=False, warnings=[], errors=[]
    )
    with pytest.raises(ReleaseSandboxValidationError, match="allowed_for_production_apply must be False"):
        validate_sandbox_activation_plan(plan)

    plan.allowed_for_production_apply = False
    plan.allowed_for_order_routing = True
    with pytest.raises(ReleaseSandboxValidationError, match="allowed_for_order_routing must be False"):
        validate_sandbox_activation_plan(plan)

    plan.allowed_for_order_routing = False
    plan.allowed_for_paper_state_mutation = True
    with pytest.raises(ReleaseSandboxValidationError, match="allowed_for_paper_state_mutation must be False"):
        validate_sandbox_activation_plan(plan)

    plan.allowed_for_paper_state_mutation = False
    validate_sandbox_activation_plan(plan) # Should pass

def test_sandbox_runtime_context_validation():
    ctx = SandboxRuntimeContext(
        context_id="c1", created_at_utc="now", sandbox_id="s1", bundle_id="b1", bundle_version="v1",
        runtime_mode=SandboxRuntimeMode.DRY_RUN_PREVIEW, in_memory_config={}, mounted_artifacts=[],
        sandbox_output_path=None, allowed_operations=[], denied_operations=[],
        allowed_to_write_production_config=True, allowed_to_mutate_paper_state=False,
        allowed_to_send_orders=False, allowed_to_send_telegram_real=False, warnings=[], errors=[]
    )
    with pytest.raises(ReleaseSandboxValidationError, match="allowed_to_write_production_config must be False"):
        validate_sandbox_runtime_context(ctx)

    ctx.allowed_to_write_production_config = False
    ctx.allowed_operations = [SandboxOperation.SEND_ORDER]
    with pytest.raises(ReleaseSandboxValidationError, match="SEND_ORDER cannot be in allowed_operations"):
        validate_sandbox_runtime_context(ctx)
