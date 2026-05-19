import pytest
from usa_signal_bot.core.enums import SandboxSafetyFlag, SandboxValidationStatus, SandboxRuntimeMode, SandboxStatus, SandboxActivationStatus
from usa_signal_bot.release_sandbox.sandbox_models import SandboxActivationPlan, SandboxRuntimeContext, SandboxMountPlan, SandboxMountMode, SandboxPreviewRun
from usa_signal_bot.release_sandbox.safety_validator import (
    validate_sandbox_activation_plan, validate_sandbox_runtime_context_safety_result,
    validate_sandbox_preview_run, sandbox_safety_validation_to_text
)

def test_safety_validator_activation_plan():
    mp = SandboxMountPlan("m1", "now", "b1", "v1", SandboxMountMode.READ_ONLY, None, None, True, True, [], [], [], [], [])
    plan = SandboxActivationPlan(
        "a1", "now", "b1", "v1", SandboxActivationStatus.VALIDATED, mp, {}, {}, {}, SandboxRuntimeMode.DRY_RUN_PREVIEW,
        False, False, False, False, [], []
    )
    val = validate_sandbox_activation_plan(plan)
    assert val.status == SandboxValidationStatus.PASS

    mp.safety_flags.append(SandboxSafetyFlag.SECRET_RISK)
    val2 = validate_sandbox_activation_plan(plan)
    assert val2.status == SandboxValidationStatus.BLOCKED

def test_safety_validator_runtime_context():
    ctx = SandboxRuntimeContext(
        context_id="c1", created_at_utc="now", sandbox_id=None, bundle_id=None, bundle_version=None,
        runtime_mode=SandboxRuntimeMode.DRY_RUN_PREVIEW, in_memory_config={}, mounted_artifacts=[],
        sandbox_output_path=None, allowed_operations=[], denied_operations=[],
        allowed_to_write_production_config=False, allowed_to_mutate_paper_state=False,
        allowed_to_send_orders=False, allowed_to_send_telegram_real=False, warnings=[], errors=[]
    )
    val = validate_sandbox_runtime_context_safety_result(ctx)
    assert val.status == SandboxValidationStatus.PASS

    ctx.allowed_to_send_orders = True
    val2 = validate_sandbox_runtime_context_safety_result(ctx)
    assert val2.status == SandboxValidationStatus.BLOCKED
    assert SandboxSafetyFlag.ORDER_ROUTING_RISK in val2.safety_flags

def test_safety_validator_preview_run():
    run = SandboxPreviewRun("r1", "now", None, None, None, SandboxRuntimeMode.DRY_RUN_PREVIEW, SandboxStatus.COMPLETED, None, [], [], [], None, None, [], [])
    val = validate_sandbox_preview_run(run)
    assert val.status == SandboxValidationStatus.PASS

    run.warnings.append("test")
    val2 = validate_sandbox_preview_run(run)
    assert val2.status == SandboxValidationStatus.WARNING

    txt = sandbox_safety_validation_to_text(val2)
    assert "WARNING" in txt
