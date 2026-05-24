from typing import Any, List, Optional
from usa_signal_bot.core.enums import PrePaperHandoffFreezeRiskFlag
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_models import (
    FinalPrePaperHandoffFreezeGate,
    SandboxRuntimeAdmissionReplayResult,
    SimulatorEvidenceFreezeBundle
)
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_gate_validator import validate_final_handoff_freeze_gate_safety

def collect_handoff_freeze_safety_flags(gate: Optional[FinalPrePaperHandoffFreezeGate] = None, replay_result: Optional[SandboxRuntimeAdmissionReplayResult] = None, freeze_bundle: Optional[SimulatorEvidenceFreezeBundle] = None) -> List[PrePaperHandoffFreezeRiskFlag]:
    flags = []
    if gate:
        if gate.sandbox_runtime_admission_allowed: flags.append(PrePaperHandoffFreezeRiskFlag.SANDBOX_RUNTIME_ADMISSION_RISK)
        if gate.paper_sandbox_runtime_allowed: flags.append(PrePaperHandoffFreezeRiskFlag.PAPER_SANDBOX_RUNTIME_RISK)
        if gate.simulator_admission_allowed: flags.append(PrePaperHandoffFreezeRiskFlag.SIMULATED_ADMISSION_RISK)
        if gate.active_paper_enabled: flags.append(PrePaperHandoffFreezeRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
        if gate.order_created: flags.append(PrePaperHandoffFreezeRiskFlag.ORDER_CREATED_RISK)
        if gate.mutation_detected: flags.append(PrePaperHandoffFreezeRiskFlag.MUTATION_DETECTED_RISK)
        if gate.allows_broker_execution: flags.append(PrePaperHandoffFreezeRiskFlag.BROKER_ORDER_RISK)
        if gate.allows_paper_state_mutation: flags.append(PrePaperHandoffFreezeRiskFlag.PAPER_STATE_MUTATION_RISK)
        if gate.allows_config_patch: flags.append(PrePaperHandoffFreezeRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
        if gate.allows_telegram_real_send: flags.append(PrePaperHandoffFreezeRiskFlag.TELEGRAM_REAL_SEND_RISK)
    if replay_result and not replay_result.passed:
        flags.append(PrePaperHandoffFreezeRiskFlag.SANDBOX_REPLAY_FAILED)
    if freeze_bundle and freeze_bundle.missing_evidence_count > 0:
        flags.append(PrePaperHandoffFreezeRiskFlag.SIMULATOR_EVIDENCE_FREEZE_FAILED)
    return list(set(flags))

def handoff_freeze_has_blocking_flags(flags: List[PrePaperHandoffFreezeRiskFlag]) -> bool:
    blocking = [
        PrePaperHandoffFreezeRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
        PrePaperHandoffFreezeRiskFlag.SANDBOX_RUNTIME_ADMISSION_RISK,
        PrePaperHandoffFreezeRiskFlag.BROKER_ORDER_RISK,
        PrePaperHandoffFreezeRiskFlag.PAPER_STATE_MUTATION_RISK,
        PrePaperHandoffFreezeRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
        PrePaperHandoffFreezeRiskFlag.TELEGRAM_REAL_SEND_RISK,
        PrePaperHandoffFreezeRiskFlag.ADMISSION_ALLOWED_RISK
    ]
    for flag in flags:
        if flag in blocking:
            return True
    return False

def validate_handoff_freeze_safety(gate: Optional[FinalPrePaperHandoffFreezeGate] = None, replay_result: Optional[SandboxRuntimeAdmissionReplayResult] = None, freeze_bundle: Optional[SimulatorEvidenceFreezeBundle] = None) -> List[str]:
    errors = []
    if gate:
        errors.extend(validate_final_handoff_freeze_gate_safety(gate))
    flags = collect_handoff_freeze_safety_flags(gate, replay_result, freeze_bundle)
    if handoff_freeze_has_blocking_flags(flags):
        errors.append("Blocking safety flags detected")
    return errors

def handoff_freeze_safety_summary(flags: List[PrePaperHandoffFreezeRiskFlag]) -> dict[str, Any]:
    return {
        "flag_count": len(flags),
        "blocking": handoff_freeze_has_blocking_flags(flags)
    }

def handoff_freeze_safety_validator_to_text(payload: dict[str, Any]) -> str:
    res = "Handoff Freeze Safety Validator\n"
    res += f"Valid: {len(payload.get('errors', [])) == 0}\n"
    return res
