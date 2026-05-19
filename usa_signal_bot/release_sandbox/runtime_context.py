import datetime
from typing import Any, Dict, List
from usa_signal_bot.release_sandbox.sandbox_models import (
    SandboxActivationPlan, SandboxRuntimeContext, create_sandbox_runtime_context_id
)
from usa_signal_bot.release_sandbox.mount_planner import default_allowed_sandbox_operations, default_denied_sandbox_operations

def mounted_artifacts_from_bundle(bundle_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return bundle_payload.get("artifacts", [])

def build_sandbox_runtime_context(
    activation_plan: SandboxActivationPlan,
    bundle_payload: Dict[str, Any]
) -> SandboxRuntimeContext:

    return SandboxRuntimeContext(
        context_id=create_sandbox_runtime_context_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        sandbox_id=activation_plan.activation_id,
        bundle_id=activation_plan.bundle_id,
        bundle_version=activation_plan.bundle_version,
        runtime_mode=activation_plan.runtime_mode,
        in_memory_config=bundle_payload.get("overlay", {}),
        mounted_artifacts=mounted_artifacts_from_bundle(bundle_payload),
        sandbox_output_path=getattr(activation_plan.mount_plan, "sandbox_output_path", None) if activation_plan.mount_plan else None,
        allowed_operations=getattr(activation_plan.mount_plan, "allowed_operations", default_allowed_sandbox_operations()),
        denied_operations=getattr(activation_plan.mount_plan, "denied_operations", default_denied_sandbox_operations()),
        allowed_to_write_production_config=False,
        allowed_to_mutate_paper_state=False,
        allowed_to_send_orders=False,
        allowed_to_send_telegram_real=False,
        warnings=[],
        errors=[]
    )

def validate_runtime_context_safety(context: SandboxRuntimeContext) -> List[str]:
    warnings = []
    if context.allowed_to_write_production_config:
        warnings.append("Context allows writing production config.")
    if context.allowed_to_mutate_paper_state:
        warnings.append("Context allows mutating paper state.")
    if context.allowed_to_send_orders:
        warnings.append("Context allows sending orders.")
    if context.allowed_to_send_telegram_real:
        warnings.append("Context allows sending real telegrams.")
    return warnings

def runtime_context_summary(context: SandboxRuntimeContext) -> Dict[str, Any]:
    return {
        "context_id": context.context_id,
        "runtime_mode": context.runtime_mode.value,
        "allowed_ops": len(context.allowed_operations),
        "artifacts_mounted": len(context.mounted_artifacts)
    }

def runtime_context_to_text(context: SandboxRuntimeContext) -> str:
    summary = runtime_context_summary(context)
    return f"Sandbox Runtime Context [{summary['context_id']}]: Mode={summary['runtime_mode']}, Artifacts={summary['artifacts_mounted']}"
