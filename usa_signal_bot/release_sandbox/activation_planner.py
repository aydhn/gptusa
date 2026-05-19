from usa_signal_bot.core.enums import SandboxStatus
import datetime
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import SandboxActivationStatus, SandboxRuntimeMode, SandboxSafetyFlag
from usa_signal_bot.release_sandbox.sandbox_models import SandboxActivationPlan, create_sandbox_activation_plan_id
from usa_signal_bot.release_sandbox.mount_planner import build_read_only_mount_plan

def build_sandbox_activation_plan(
    bundle_payload: Dict[str, Any],
    source_bundle_path: Optional[str] = None,
    sandbox_output_path: Optional[str] = None,
    runtime_mode: SandboxRuntimeMode = SandboxRuntimeMode.FULL_SAFE_PREVIEW
) -> SandboxActivationPlan:

    manifest = bundle_payload.get("manifest", {})
    mount_plan = build_read_only_mount_plan(bundle_payload, source_bundle_path, sandbox_output_path)

    status = SandboxActivationStatus.VALIDATED
    # Evaluate flags
    if mount_plan.safety_flags:
        status = SandboxActivationStatus.BLOCKED

    return SandboxActivationPlan(
        activation_id=create_sandbox_activation_plan_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        bundle_id=manifest.get("bundle_id"),
        bundle_version=manifest.get("bundle_version"),
        status=status,
        mount_plan=mount_plan,
        bundle_validation_summary=bundle_payload.get("validation", {}),
        compatibility_summary={},
        safety_summary={},
        runtime_mode=runtime_mode,
        manual_review_required=False,
        allowed_for_production_apply=False,
        allowed_for_order_routing=False,
        allowed_for_paper_state_mutation=False,
        warnings=[],
        errors=[]
    )

def activation_allowed(plan: SandboxActivationPlan) -> bool:
    return plan.status in [SandboxActivationStatus.VALIDATED, SandboxStatus.READY]

def activation_block_reasons(plan: SandboxActivationPlan) -> List[str]:
    reasons = []
    if plan.status == SandboxActivationStatus.BLOCKED:
        reasons.append("Status is BLOCKED.")
    if plan.allowed_for_production_apply or plan.allowed_for_order_routing or plan.allowed_for_paper_state_mutation:
        reasons.append("Unsafe flags are set to True.")
    return reasons

def activation_plan_summary(plan: SandboxActivationPlan) -> Dict[str, Any]:
    return {
        "activation_id": plan.activation_id,
        "status": plan.status.value,
        "runtime_mode": plan.runtime_mode.value,
        "is_allowed": activation_allowed(plan)
    }

def activation_plan_to_text(plan: SandboxActivationPlan) -> str:
    summary = activation_plan_summary(plan)
    return f"Activation Plan [{summary['activation_id']}]: Status={summary['status']}, Allowed={summary['is_allowed']}"
