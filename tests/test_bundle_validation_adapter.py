import pytest
from usa_signal_bot.core.enums import SandboxSafetyFlag, SandboxValidationStatus
from usa_signal_bot.release_sandbox.bundle_validation_adapter import (
    sandbox_validation_from_bundle_validation, map_bundle_safety_flags_to_sandbox_flags,
    bundle_validation_adapter_to_text
)

def test_bundle_validation_adapter():
    bundle_payload = {
        "status": "PASS",
        "bundle_id": "b1",
        "safety_flags": ["SECRET_RISK", "UNKNOWN_FLAG"]
    }

    mapped = map_bundle_safety_flags_to_sandbox_flags(["SECRET_RISK", "UNKNOWN_FLAG"])
    assert SandboxSafetyFlag.SECRET_RISK in mapped
    assert SandboxSafetyFlag.UNKNOWN in mapped

    val = sandbox_validation_from_bundle_validation(bundle_payload)
    assert val.status == SandboxValidationStatus.PASS
    assert SandboxSafetyFlag.SECRET_RISK in val.safety_flags

    bundle_payload["status"] = "BLOCKED"
    val2 = sandbox_validation_from_bundle_validation(bundle_payload)
    assert val2.status == SandboxValidationStatus.BLOCKED

    txt = bundle_validation_adapter_to_text(bundle_payload)
    assert "BLOCKED" in txt
    assert "Blocks Sandbox=True" in txt
