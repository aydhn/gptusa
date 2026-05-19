import datetime
from typing import Any, Dict, List
from usa_signal_bot.release_sandbox.sandbox_models import SandboxRuntimeContext, SandboxActivationPlan, create_sandbox_runtime_context_id
from usa_signal_bot.release_sandbox.mount_planner import default_allowed_sandbox_operations, default_denied_sandbox_operations

def build_sandbox_runtime_context(activation_plan: SandboxActivationPlan, bundle_payload: Dict[str, Any]) -> SandboxRuntimeContext:
    return SandboxRuntimeContext(
        context_id=create_sandbox_runtime_context_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        sandbox_id=activation_plan.activation_id,
        bundle_id=activation_plan.bundle_id,
        bundle_version=activation_plan.bundle_version,
        runtime_mode=activation_plan.runtime_mode,
        in_memory_config={"preview": True},
        mounted_artifacts=[],
        sandbox_output_path=activation_plan.mount_plan.sandbox_output_path if activation_plan.mount_plan else None,
        allowed_operations=default_allowed_sandbox_operations(),
        denied_operations=default_denied_sandbox_operations(),
        allowed_to_write_production_config=False,
        allowed_to_mutate_paper_state=False,
        allowed_to_send_orders=False,
        allowed_to_send_telegram_real=False,
        warnings=[],
        errors=[]
    )

def mounted_artifacts_from_bundle(bundle_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return []

def validate_runtime_context_safety(context: SandboxRuntimeContext) -> List[str]:
    return []

def runtime_context_summary(context: SandboxRuntimeContext) -> Dict[str, Any]:
    return {"context_id": context.context_id}

def runtime_context_to_text(context: SandboxRuntimeContext) -> str:
    return f"Runtime Context {context.context_id}"
