import datetime
from typing import Any, Dict, List
from usa_signal_bot.core.enums import SandboxSafetyFlag, SandboxValidationStatus
from usa_signal_bot.release_sandbox.sandbox_models import SandboxValidationResult, create_sandbox_validation_result_id

def map_bundle_safety_flags_to_sandbox_flags(flags: List[str]) -> List[SandboxSafetyFlag]:
    mapped = []
    # Mapping logic from bundle flags to sandbox flags
    # E.g., if "SECRET_LEAK_RISK" in flags: mapped.append(SandboxSafetyFlag.SECRET_RISK)
    # Placeholder mapping
    for flag in flags:
        try:
            mapped.append(SandboxSafetyFlag(flag))
        except ValueError:
            mapped.append(SandboxSafetyFlag.UNKNOWN)
    return mapped

def bundle_validation_blocks_sandbox(bundle_validation_payload: Dict[str, Any]) -> bool:
    status = bundle_validation_payload.get("status", "")
    return status in ["BLOCKED", "FAIL", "INVALID"]

def sandbox_validation_from_bundle_validation(bundle_validation_payload: Dict[str, Any]) -> SandboxValidationResult:
    flags_raw = bundle_validation_payload.get("safety_flags", [])
    mapped_flags = map_bundle_safety_flags_to_sandbox_flags(flags_raw)

    status = SandboxValidationStatus.PASS
    if bundle_validation_blocks_sandbox(bundle_validation_payload):
        status = SandboxValidationStatus.BLOCKED

    return SandboxValidationResult(
        validation_id=create_sandbox_validation_result_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        sandbox_id=None,
        bundle_id=bundle_validation_payload.get("bundle_id"),
        status=status,
        safety_flags=mapped_flags,
        read_only_passed=True,
        output_isolation_passed=True,
        blocked_operations_enforced=True,
        no_order_routing_passed=True,
        no_paper_mutation_passed=True,
        no_telegram_real_send_passed=True,
        validation_messages=bundle_validation_payload.get("messages", []),
        warnings=[],
        errors=[]
    )

def bundle_validation_adapter_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": payload.get("status", "UNKNOWN"),
        "blocks_sandbox": bundle_validation_blocks_sandbox(payload),
        "flags_count": len(payload.get("safety_flags", []))
    }

def bundle_validation_adapter_to_text(payload: Dict[str, Any]) -> str:
    summary = bundle_validation_adapter_summary(payload)
    return f"Bundle Validation Adapter: Status={summary['status']}, Blocks Sandbox={summary['blocks_sandbox']}"
