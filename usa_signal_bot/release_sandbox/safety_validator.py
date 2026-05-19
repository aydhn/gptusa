import datetime
from typing import Any, Dict, List
from usa_signal_bot.core.enums import SandboxSafetyFlag, SandboxValidationStatus
from usa_signal_bot.release_sandbox.sandbox_models import (
    SandboxActivationPlan, SandboxRuntimeContext, SandboxPreviewRun,
    SandboxValidationResult, create_sandbox_validation_result_id
)

def collect_sandbox_safety_flags_from_plan(plan: SandboxActivationPlan) -> List[SandboxSafetyFlag]:
    flags = []
    if getattr(plan, "mount_plan", None):
        flags.extend(plan.mount_plan.safety_flags)
    return list(set(flags))

def collect_sandbox_safety_flags_from_context(context: SandboxRuntimeContext) -> List[SandboxSafetyFlag]:
    flags = []
    if context.allowed_to_send_orders:
        flags.append(SandboxSafetyFlag.ORDER_ROUTING_RISK)
    if context.allowed_to_mutate_paper_state:
        flags.append(SandboxSafetyFlag.PAPER_STATE_MUTATION_RISK)
    if context.allowed_to_send_telegram_real:
        flags.append(SandboxSafetyFlag.TELEGRAM_REAL_SEND_RISK)
    if context.allowed_to_write_production_config:
        flags.append(SandboxSafetyFlag.PRODUCTION_PATCH_RISK)
    return flags

def validate_sandbox_activation_plan(plan: SandboxActivationPlan) -> SandboxValidationResult:
    flags = collect_sandbox_safety_flags_from_plan(plan)
    status = SandboxValidationStatus.PASS
    if flags:
        status = SandboxValidationStatus.BLOCKED

    return SandboxValidationResult(
        validation_id=create_sandbox_validation_result_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        sandbox_id=plan.activation_id,
        bundle_id=plan.bundle_id,
        status=status,
        safety_flags=flags,
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

def validate_sandbox_runtime_context_safety_result(context: SandboxRuntimeContext) -> SandboxValidationResult:
    flags = collect_sandbox_safety_flags_from_context(context)
    status = SandboxValidationStatus.PASS
    if flags:
        status = SandboxValidationStatus.BLOCKED

    return SandboxValidationResult(
        validation_id=create_sandbox_validation_result_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        sandbox_id=context.sandbox_id,
        bundle_id=context.bundle_id,
        status=status,
        safety_flags=flags,
        read_only_passed=True,
        output_isolation_passed=True,
        blocked_operations_enforced=True,
        no_order_routing_passed=not context.allowed_to_send_orders,
        no_paper_mutation_passed=not context.allowed_to_mutate_paper_state,
        no_telegram_real_send_passed=not context.allowed_to_send_telegram_real,
        validation_messages=[],
        warnings=[],
        errors=[]
    )

def validate_sandbox_preview_run(run: SandboxPreviewRun) -> SandboxValidationResult:
    status = SandboxValidationStatus.PASS
    if run.warnings:
        status = SandboxValidationStatus.WARNING
    if run.errors:
        status = SandboxValidationStatus.FAIL

    return SandboxValidationResult(
        validation_id=create_sandbox_validation_result_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        sandbox_id=run.sandbox_id,
        bundle_id=run.bundle_id,
        status=status,
        safety_flags=run.safety_flags,
        read_only_passed=True,
        output_isolation_passed=True,
        blocked_operations_enforced=True,
        no_order_routing_passed=True,
        no_paper_mutation_passed=True,
        no_telegram_real_send_passed=True,
        validation_messages=[],
        warnings=run.warnings,
        errors=run.errors
    )

def sandbox_safety_validation_to_text(result: SandboxValidationResult) -> str:
    return f"Sandbox Validation [{result.validation_id}]: Status={result.status.value}, Flags={len(result.safety_flags)}"
