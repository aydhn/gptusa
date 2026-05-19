import datetime
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import SandboxMountMode, SandboxOperation, SandboxSafetyFlag
from usa_signal_bot.release_sandbox.sandbox_models import SandboxMountPlan, create_sandbox_mount_plan_id

def default_allowed_sandbox_operations() -> List[SandboxOperation]:
    return [
        SandboxOperation.READ_BUNDLE,
        SandboxOperation.READ_MANIFEST,
        SandboxOperation.READ_ARTIFACTS,
        SandboxOperation.BUILD_IN_MEMORY_CONFIG,
        SandboxOperation.RUN_SIGNAL_PREVIEW,
        SandboxOperation.RUN_PORTFOLIO_PREVIEW,
        SandboxOperation.RUN_RISK_PREVIEW,
        SandboxOperation.GENERATE_NOTIFICATION_PREVIEW,
        SandboxOperation.WRITE_SANDBOX_OUTPUT
    ]

def default_denied_sandbox_operations() -> List[SandboxOperation]:
    return [
        SandboxOperation.WRITE_PRODUCTION_CONFIG,
        SandboxOperation.MUTATE_PAPER_STATE,
        SandboxOperation.SEND_ORDER,
        SandboxOperation.SEND_TELEGRAM_REAL,
        SandboxOperation.NETWORK_BROKER_CALL
    ]

def build_read_only_mount_plan(bundle_payload: Dict[str, Any], source_bundle_path: Optional[str] = None, sandbox_output_path: Optional[str] = None) -> SandboxMountPlan:
    return SandboxMountPlan(
        mount_id=create_sandbox_mount_plan_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        bundle_id=bundle_payload.get("id"),
        bundle_version=bundle_payload.get("version"),
        mount_mode=SandboxMountMode.READ_ONLY,
        source_bundle_path=source_bundle_path,
        sandbox_output_path=sandbox_output_path,
        read_only_verified=True,
        copy_on_write_enabled=True,
        allowed_operations=default_allowed_sandbox_operations(),
        denied_operations=default_denied_sandbox_operations(),
        safety_flags=[],
        warnings=[],
        errors=[]
    )

def mount_plan_safety_flags(plan: SandboxMountPlan) -> List[SandboxSafetyFlag]:
    return plan.safety_flags

def mount_plan_summary(plan: SandboxMountPlan) -> Dict[str, Any]:
    return {"mount_id": plan.mount_id, "mode": plan.mount_mode}

def mount_plan_to_text(plan: SandboxMountPlan) -> str:
    return f"Mount Plan {plan.mount_id} - Mode: {plan.mount_mode}"
