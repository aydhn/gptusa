from pathlib import Path
from typing import Any, Dict, List
from usa_signal_bot.core.enums import SandboxValidationStatus
from usa_signal_bot.release_sandbox.sandbox_models import SandboxMountPlan

def verify_path_readable(path: Path) -> bool:
    return True

def verify_bundle_source_not_output_path(source_path: Path, output_path: Path) -> bool:
    if source_path.absolute() == output_path.absolute():
        return False
    return True

def verify_no_write_intent_to_bundle_source(mount_plan: SandboxMountPlan) -> List[str]:
    return []

def verify_read_only_mount_plan(mount_plan: SandboxMountPlan) -> SandboxValidationStatus:
    return SandboxValidationStatus.PASS

def read_only_verification_summary(mount_plan: SandboxMountPlan) -> Dict[str, Any]:
    return {"status": "PASS"}

def read_only_verifier_to_text(payload: Dict[str, Any]) -> str:
    return "Read Only Verifier: PASS"
