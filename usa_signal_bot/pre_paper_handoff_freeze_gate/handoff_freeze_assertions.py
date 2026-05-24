from typing import Any, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import HandoffFreezeAssertionStatus
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_models import (
    HandoffFreezeAssertion,
    SandboxRuntimeAdmissionReplayResult,
    SimulatorEvidenceFreezeBundle,
    create_handoff_freeze_assertion_id
)

def required_handoff_freeze_assertions() -> List[str]:
    return [
        "assertion_metadata_only_handoff",
        "assertion_no_sandbox_runtime_admission",
        "assertion_no_paper_sandbox_runtime",
        "assertion_no_simulator_admission",
        "assertion_no_local_paper_simulator",
        "assertion_no_active_paper",
        "assertion_no_paper_admission",
        "assertion_no_order",
        "assertion_no_write",
        "assertion_no_broker",
        "assertion_no_config_patch",
        "assertion_no_telegram_real_send",
        "assertion_phase_100_frozen_handoff"
    ]

def build_handoff_freeze_assertions(payload: dict[str, Any], replay_result: Optional[SandboxRuntimeAdmissionReplayResult] = None, freeze_bundle: Optional[SimulatorEvidenceFreezeBundle] = None) -> List[HandoffFreezeAssertion]:
    return [
        assertion_metadata_only_handoff(payload),
        assertion_no_sandbox_runtime_admission(payload),
        assertion_no_paper_sandbox_runtime(payload),
        assertion_no_simulator_admission(payload),
        assertion_no_local_paper_simulator(payload),
        assertion_no_active_paper(payload),
        assertion_no_paper_admission(payload),
        assertion_no_order(payload),
        assertion_no_write(payload),
        assertion_no_broker(payload),
        assertion_no_config_patch(payload),
        assertion_no_telegram_real_send(payload),
        assertion_phase_100_frozen_handoff(payload)
    ]

def _create_assertion(name: str, passed: bool, desc: str) -> HandoffFreezeAssertion:
    return HandoffFreezeAssertion(
        assertion_id=create_handoff_freeze_assertion_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        assertion_name=name,
        status=HandoffFreezeAssertionStatus.PASS if passed else HandoffFreezeAssertionStatus.FAIL,
        expected_value=True,
        observed_value=passed,
        description=desc,
        risk_flags=[],
        warnings=[],
        errors=[] if passed else [f"Assertion {name} failed"]
    )

def assertion_metadata_only_handoff(payload: dict[str, Any]) -> HandoffFreezeAssertion:
    passed = payload.get("handoff_is_metadata_only", True)
    return _create_assertion("assertion_metadata_only_handoff", passed, "Handoff must be metadata only")

def assertion_no_sandbox_runtime_admission(payload: dict[str, Any]) -> HandoffFreezeAssertion:
    passed = not payload.get("sandbox_runtime_admission_allowed", False)
    return _create_assertion("assertion_no_sandbox_runtime_admission", passed, "Sandbox runtime admission must not be allowed")

def assertion_no_paper_sandbox_runtime(payload: dict[str, Any]) -> HandoffFreezeAssertion:
    passed = not payload.get("paper_sandbox_runtime_allowed", False)
    return _create_assertion("assertion_no_paper_sandbox_runtime", passed, "Paper sandbox runtime must not be allowed")

def assertion_no_simulator_admission(payload: dict[str, Any]) -> HandoffFreezeAssertion:
    passed = not payload.get("simulator_admission_allowed", False)
    return _create_assertion("assertion_no_simulator_admission", passed, "Simulator admission must not be allowed")

def assertion_no_local_paper_simulator(payload: dict[str, Any]) -> HandoffFreezeAssertion:
    passed = not payload.get("local_paper_simulator_allowed", False)
    return _create_assertion("assertion_no_local_paper_simulator", passed, "Local paper simulator must not be allowed")

def assertion_no_active_paper(payload: dict[str, Any]) -> HandoffFreezeAssertion:
    passed = not payload.get("active_paper_enabled", False)
    return _create_assertion("assertion_no_active_paper", passed, "Active paper must not be enabled")

def assertion_no_paper_admission(payload: dict[str, Any]) -> HandoffFreezeAssertion:
    passed = not payload.get("admission_allowed", False)
    return _create_assertion("assertion_no_paper_admission", passed, "Paper admission must not be allowed")

def assertion_no_order(payload: dict[str, Any]) -> HandoffFreezeAssertion:
    passed = not payload.get("order_created", False)
    return _create_assertion("assertion_no_order", passed, "Order must not be created")

def assertion_no_write(payload: dict[str, Any]) -> HandoffFreezeAssertion:
    passed = not payload.get("mutation_detected", False)
    return _create_assertion("assertion_no_write", passed, "No state mutation should be detected")

def assertion_no_broker(payload: dict[str, Any]) -> HandoffFreezeAssertion:
    passed = not payload.get("allows_broker_execution", False)
    return _create_assertion("assertion_no_broker", passed, "Broker execution must not be allowed")

def assertion_no_config_patch(payload: dict[str, Any]) -> HandoffFreezeAssertion:
    passed = not payload.get("allows_config_patch", False)
    return _create_assertion("assertion_no_config_patch", passed, "Config patching must not be allowed")

def assertion_no_telegram_real_send(payload: dict[str, Any]) -> HandoffFreezeAssertion:
    passed = not payload.get("allows_telegram_real_send", False)
    return _create_assertion("assertion_no_telegram_real_send", passed, "Real telegram send must not be allowed")

def assertion_phase_100_frozen_handoff(payload: dict[str, Any]) -> HandoffFreezeAssertion:
    passed = payload.get("pre_paper_handoff_complete", True)
    return _create_assertion("assertion_phase_100_frozen_handoff", passed, "Phase 100 handoff must be marked complete (frozen)")

def handoff_freeze_assertions_summary(assertions: List[HandoffFreezeAssertion]) -> dict[str, Any]:
    passed = sum(1 for a in assertions if a.status == HandoffFreezeAssertionStatus.PASS)
    return {
        "total": len(assertions),
        "passed": passed,
        "failed": len(assertions) - passed
    }

def handoff_freeze_assertions_to_text(assertions: List[HandoffFreezeAssertion], limit: int = 100) -> str:
    res = "Handoff Freeze Assertions:\n"
    for a in assertions[:limit]:
        res += f"- {a.assertion_name}: {a.status.value}\n"
    return res
