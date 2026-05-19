import datetime
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import SandboxActivationStatus, SandboxRuntimeMode
from usa_signal_bot.release_sandbox.sandbox_models import SandboxActivationPlan, create_sandbox_activation_plan_id
from usa_signal_bot.release_sandbox.mount_planner import build_read_only_mount_plan

def build_sandbox_activation_plan(bundle_payload: Dict[str, Any], source_bundle_path: Optional[str] = None, sandbox_output_path: Optional[str] = None, runtime_mode: SandboxRuntimeMode = SandboxRuntimeMode.FULL_SAFE_PREVIEW) -> SandboxActivationPlan:
    mount_plan = build_read_only_mount_plan(bundle_payload, source_bundle_path, sandbox_output_path)
    return SandboxActivationPlan(
        activation_id=create_sandbox_activation_plan_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        bundle_id=bundle_payload.get("id"),
        bundle_version=bundle_payload.get("version"),
        status=SandboxActivationStatus.READY if not mount_plan.errors else SandboxActivationStatus.BLOCKED,
        mount_plan=mount_plan,
        bundle_validation_summary={},
        compatibility_summary={},
        safety_summary={},
        runtime_mode=runtime_mode,
        manual_review_required=True,
        allowed_for_production_apply=False,
        allowed_for_order_routing=False,
        allowed_for_paper_state_mutation=False,
        warnings=[],
        errors=[]
    )

def activation_allowed(plan: SandboxActivationPlan) -> bool:
    return not plan.errors and plan.status != SandboxActivationStatus.BLOCKED

def activation_block_reasons(plan: SandboxActivationPlan) -> List[str]:
    return plan.errors

def activation_plan_summary(plan: SandboxActivationPlan) -> Dict[str, Any]:
    return {"activation_id": plan.activation_id, "status": plan.status}

def activation_plan_to_text(plan: SandboxActivationPlan) -> str:
    return f"Activation Plan {plan.activation_id} - Status: {plan.status}"
