from typing import Any, List
from usa_signal_bot.core.enums import (
    PrePaperHandoffFreezeGateDecision,
    PrePaperHandoffFreezeGateStatus,
    PrePaperHandoffFreezeRiskFlag
)
from usa_signal_bot.pre_paper_handoff_freeze_gate.simulator_dossier_ingestion import simulator_dossier_supports_handoff_freeze

def evaluate_handoff_freeze_gate_eligibility(payload: dict[str, Any]) -> PrePaperHandoffFreezeGateDecision:
    valid, warnings = simulator_dossier_supports_handoff_freeze(payload)

    if not valid:
        return PrePaperHandoffFreezeGateDecision.REJECT

    if "sandbox_replay_missing" in warnings or "sandbox_replay_failed" in warnings:
        return PrePaperHandoffFreezeGateDecision.REQUEST_SANDBOX_REPLAY

    if "simulator_evidence_freeze_missing" in warnings or "simulator_evidence_freeze_stale" in warnings:
        return PrePaperHandoffFreezeGateDecision.REQUEST_SIMULATOR_EVIDENCE_FREEZE

    if "simulator_dossier_missing" in warnings or "simulator_dossier_stale" in warnings or "simulator_dossier_failed" in warnings:
        return PrePaperHandoffFreezeGateDecision.REQUEST_SIMULATOR_DOSSIER_REFRESH

    if payload.get("manual_review_missing", False):
        return PrePaperHandoffFreezeGateDecision.REQUEST_MANUAL_REVIEW

    if warnings:
        return PrePaperHandoffFreezeGateDecision.BLOCK

    return PrePaperHandoffFreezeGateDecision.COMPLETE_PRE_PAPER_HANDOFF_FREEZE

def handoff_freeze_gate_eligibility_reasons(payload: dict[str, Any]) -> List[str]:
    _, warnings = simulator_dossier_supports_handoff_freeze(payload)
    return warnings

def handoff_freeze_safety_flags_from_payload(payload: dict[str, Any]) -> List[PrePaperHandoffFreezeRiskFlag]:
    flags = []
    if payload.get("sandbox_runtime_admission_allowed"):
        flags.append(PrePaperHandoffFreezeRiskFlag.SANDBOX_RUNTIME_ADMISSION_RISK)
    if payload.get("paper_sandbox_runtime_allowed"):
        flags.append(PrePaperHandoffFreezeRiskFlag.PAPER_SANDBOX_RUNTIME_RISK)
    if payload.get("simulator_admission_allowed"):
        flags.append(PrePaperHandoffFreezeRiskFlag.SIMULATED_ADMISSION_RISK)
    if payload.get("local_paper_simulator_allowed"):
        flags.append(PrePaperHandoffFreezeRiskFlag.LOCAL_PAPER_SIMULATOR_RISK)
    if payload.get("admission_allowed"):
        flags.append(PrePaperHandoffFreezeRiskFlag.ADMISSION_ALLOWED_RISK)
    if payload.get("activation_allowed"):
        flags.append(PrePaperHandoffFreezeRiskFlag.ACTIVATION_ALLOWED_RISK)
    if payload.get("transition_allowed"):
        flags.append(PrePaperHandoffFreezeRiskFlag.TRANSITION_ALLOWED_RISK)
    if payload.get("order_created"):
        flags.append(PrePaperHandoffFreezeRiskFlag.ORDER_CREATED_RISK)
    if payload.get("mutation_detected"):
        flags.append(PrePaperHandoffFreezeRiskFlag.MUTATION_DETECTED_RISK)
    return flags

def handoff_freeze_gate_status_from_decision(decision: PrePaperHandoffFreezeGateDecision) -> PrePaperHandoffFreezeGateStatus:
    if decision == PrePaperHandoffFreezeGateDecision.COMPLETE_PRE_PAPER_HANDOFF_FREEZE:
        return PrePaperHandoffFreezeGateStatus.VALIDATED_HANDOFF_FROZEN
    if decision in [PrePaperHandoffFreezeGateDecision.REQUEST_SANDBOX_REPLAY, PrePaperHandoffFreezeGateDecision.REQUEST_SIMULATOR_EVIDENCE_FREEZE, PrePaperHandoffFreezeGateDecision.REQUEST_SIMULATOR_DOSSIER_REFRESH, PrePaperHandoffFreezeGateDecision.REQUEST_MANUAL_REVIEW]:
        return PrePaperHandoffFreezeGateStatus.REQUEST_CHANGES
    if decision == PrePaperHandoffFreezeGateDecision.REJECT:
        return PrePaperHandoffFreezeGateStatus.REJECTED
    if decision == PrePaperHandoffFreezeGateDecision.BLOCK:
        return PrePaperHandoffFreezeGateStatus.BLOCKED
    return PrePaperHandoffFreezeGateStatus.UNKNOWN

def eligibility_checker_to_text(payload: dict[str, Any]) -> str:
    decision = evaluate_handoff_freeze_gate_eligibility(payload)
    reasons = handoff_freeze_gate_eligibility_reasons(payload)
    flags = handoff_freeze_safety_flags_from_payload(payload)

    res = f"Handoff Freeze Eligibility Checker\nDecision: {decision.value}\n"
    if reasons:
        res += "Reasons:\n"
        for r in reasons:
            res += f"- {r}\n"
    if flags:
        res += "Flags:\n"
        for f in flags:
            res += f"- {f.value}\n"
    return res
