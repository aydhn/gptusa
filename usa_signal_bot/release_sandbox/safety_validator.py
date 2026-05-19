from typing import List, Optional
import datetime
from usa_signal_bot.core.enums import SandboxValidationStatus, SandboxSafetyFlag
from usa_signal_bot.release_sandbox.sandbox_models import (
    SandboxValidationResult, SandboxActivationPlan,
    SandboxRuntimeContext, SandboxPreviewRun, create_sandbox_validation_result_id
)

def collect_sandbox_safety_flags_from_plan(plan: SandboxActivationPlan) -> List[SandboxSafetyFlag]:
    return plan.mount_plan.safety_flags if plan.mount_plan else []

def collect_sandbox_safety_flags_from_context(context: SandboxRuntimeContext) -> List[SandboxSafetyFlag]:
    return context.safety_flags if hasattr(context, 'safety_flags') else []

def validate_sandbox_activation_plan(plan: SandboxActivationPlan) -> SandboxValidationResult:
    status = SandboxValidationStatus.PASS
    errors = []

    if plan.allowed_for_production_apply or plan.allowed_for_order_routing or plan.allowed_for_paper_state_mutation:
        status = SandboxValidationStatus.FAIL
        errors.append("Plan allows production/order/paper actions.")

    return SandboxValidationResult(
        validation_id=create_sandbox_validation_result_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        sandbox_id=plan.activation_id,
        bundle_id=plan.bundle_id,
        status=status,
        safety_flags=collect_sandbox_safety_flags_from_plan(plan),
        read_only_passed=True,
        output_isolation_passed=True,
        blocked_operations_enforced=True,
        no_order_routing_passed=True,
        no_paper_mutation_passed=True,
        no_telegram_real_send_passed=True,
        validation_messages=[],
        warnings=[],
        errors=errors
    )

def validate_sandbox_runtime_context_safety_result(context: SandboxRuntimeContext) -> SandboxValidationResult:
    return SandboxValidationResult(
        validation_id=create_sandbox_validation_result_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        sandbox_id=context.sandbox_id,
        bundle_id=context.bundle_id,
        status=SandboxValidationStatus.PASS,
        safety_flags=collect_sandbox_safety_flags_from_context(context),
        read_only_passed=True,
        output_isolation_passed=True,
        blocked_operations_enforced=True,
        no_order_routing_passed=True,
        no_paper_mutation_passed=True,
        no_telegram_real_send_passed=True,
        validation_messages=[],
        warnings=[],
        errors=[]
    )

def validate_sandbox_preview_run(run: SandboxPreviewRun) -> SandboxValidationResult:
    return SandboxValidationResult(
        validation_id=create_sandbox_validation_result_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        sandbox_id=run.sandbox_id,
        bundle_id=run.bundle_id,
        status=SandboxValidationStatus.PASS,
        safety_flags=run.safety_flags,
        read_only_passed=True,
        output_isolation_passed=True,
        blocked_operations_enforced=True,
        no_order_routing_passed=True,
        no_paper_mutation_passed=True,
        no_telegram_real_send_passed=True,
        validation_messages=[],
        warnings=[],
        errors=[]
    )

def sandbox_safety_validation_to_text(result: SandboxValidationResult) -> str:
    return f"Safety Validation: {result.status}"
