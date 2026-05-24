from typing import Any, List, Optional
from usa_signal_bot.core.enums import PrePaperHandoffFreezeRiskFlag
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_models import (
    FinalPrePaperHandoffFreezeGate,
    SandboxRuntimeAdmissionReplayResult,
    SimulatorEvidenceFreezeBundle
)

def validate_handoff_freeze_continuity(gate: Optional[FinalPrePaperHandoffFreezeGate] = None, replay_result: Optional[SandboxRuntimeAdmissionReplayResult] = None, freeze_bundle: Optional[SimulatorEvidenceFreezeBundle] = None) -> List[str]:
    errors = []
    if gate:
        if not gate.activation_denied: errors.append("activation_denied must be true")
        if gate.activation_allowed: errors.append("activation_allowed must be false")
        if gate.admission_allowed: errors.append("admission_allowed must be false")
        if gate.transition_allowed: errors.append("transition_allowed must be false")
        if gate.sandbox_runtime_admission_allowed: errors.append("sandbox_runtime_admission_allowed must be false")
        if gate.paper_sandbox_runtime_allowed: errors.append("paper_sandbox_runtime_allowed must be false")
        if gate.simulator_admission_allowed: errors.append("simulator_admission_allowed must be false")
        if gate.local_paper_simulator_allowed: errors.append("local_paper_simulator_allowed must be false")
        if gate.active_paper_enabled: errors.append("active_paper_enabled must be false")
        if not gate.all_writes_blocked: errors.append("all_writes_blocked must be true")
        if gate.order_created: errors.append("order_created must be false")
        if gate.mutation_detected: errors.append("mutation_detected must be false")
        if gate.allows_active_paper: errors.append("allows_active_paper must be false")
        if gate.allows_broker_execution: errors.append("allows_broker_execution must be false")
        if gate.allows_paper_state_mutation: errors.append("allows_paper_state_mutation must be false")
        if gate.allows_config_patch: errors.append("allows_config_patch must be false")
        if gate.allows_telegram_real_send: errors.append("allows_telegram_real_send must be false")

    if replay_result and not replay_result.passed:
        errors.append("Sandbox runtime admission replay did not pass")

    if freeze_bundle and freeze_bundle.missing_evidence_count > 0:
        errors.append("Simulator evidence freeze is missing items")

    return errors

def handoff_freeze_continuity_flags(payload: dict[str, Any]) -> List[PrePaperHandoffFreezeRiskFlag]:
    flags = []
    # Implementation depends on payload contents, typically we map violations to risk flags here
    return flags

def handoff_freeze_continuity_is_preserved(payload: dict[str, Any]) -> bool:
    return len(validate_handoff_freeze_continuity(payload.get("gate"))) == 0

def handoff_freeze_continuity_summary(payload: dict[str, Any]) -> dict[str, Any]:
    errors = validate_handoff_freeze_continuity(payload.get("gate"))
    return {
        "preserved": len(errors) == 0,
        "errors": errors
    }

def handoff_freeze_continuity_to_text(payload: dict[str, Any]) -> str:
    errors = validate_handoff_freeze_continuity(payload.get("gate"))
    res = f"Handoff Freeze Continuity: {'Preserved' if not errors else 'Broken'}\n"
    if errors:
        for e in errors:
            res += f"- {e}\n"
    return res
