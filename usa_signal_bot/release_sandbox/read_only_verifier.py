import os
from pathlib import Path
from typing import Any, Dict, List
from usa_signal_bot.core.enums import SandboxValidationStatus
from usa_signal_bot.release_sandbox.sandbox_models import SandboxMountPlan

def verify_path_readable(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        return os.access(path, os.R_OK)
    except Exception:
        return False

def verify_bundle_source_not_output_path(source_path: Path, output_path: Path) -> bool:
    try:
        return source_path.resolve() != output_path.resolve()
    except Exception:
        return True

def verify_no_write_intent_to_bundle_source(mount_plan: SandboxMountPlan) -> List[str]:
    warnings = []
    # Any write intent checking logic could be implemented here
    # For now, it's just checking if it is enabled in plan
    if not mount_plan.read_only_verified:
        warnings.append("Mount plan read_only is not verified.")
    return warnings

def verify_read_only_mount_plan(mount_plan: SandboxMountPlan) -> SandboxValidationStatus:
    if mount_plan.source_bundle_path and mount_plan.sandbox_output_path:
        source_path = Path(mount_plan.source_bundle_path)
        output_path = Path(mount_plan.sandbox_output_path)

        if not verify_bundle_source_not_output_path(source_path, output_path):
            return SandboxValidationStatus.FAIL

    if verify_no_write_intent_to_bundle_source(mount_plan):
        return SandboxValidationStatus.WARNING

    return SandboxValidationStatus.PASS

def read_only_verification_summary(mount_plan: SandboxMountPlan) -> Dict[str, Any]:
    return {
        "mount_id": mount_plan.mount_id,
        "read_only_status": verify_read_only_mount_plan(mount_plan).value,
        "source_path": mount_plan.source_bundle_path,
        "output_path": mount_plan.sandbox_output_path
    }

def read_only_verifier_to_text(payload: Dict[str, Any]) -> str:
    return f"Read-only Verification: Status={payload['read_only_status']} (Source: {payload['source_path']}, Output: {payload['output_path']})"
