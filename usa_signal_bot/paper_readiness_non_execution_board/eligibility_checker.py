from typing import Any, Dict, List
from usa_signal_bot.core.enums import PaperReadinessNonExecutionBoardDecision, PaperReadinessNonExecutionBoardStatus, NonExecutionBoardRiskFlag
from usa_signal_bot.paper_readiness_non_execution_board.dossier_ingestion import paper_safe_dossier_supports_non_execution_board

def evaluate_non_execution_board_eligibility(dossier_payload: Dict[str, Any]) -> PaperReadinessNonExecutionBoardDecision:
    valid, warnings = paper_safe_dossier_supports_non_execution_board(dossier_payload)

    if not valid:
        if "Missing non-execution acceptance seal" in warnings or "Non-execution acceptance seal is invalid" in warnings:
            return PaperReadinessNonExecutionBoardDecision.REQUEST_SEAL_INTEGRITY_AUDIT
        if "Missing pre-paper runtime map" in warnings or "Runtime map outcome is not MAP_VERIFIED_SAFE" in warnings:
            return PaperReadinessNonExecutionBoardDecision.REQUEST_RUNTIME_MAP_REPLAY
        return PaperReadinessNonExecutionBoardDecision.REQUEST_PAPER_SAFE_DOSSIER_REFRESH

    return PaperReadinessNonExecutionBoardDecision.PASS_TO_NON_EXECUTION_BOARD_DOSSIER

def non_execution_board_eligibility_reasons(dossier_payload: Dict[str, Any]) -> List[str]:
    _, warnings = paper_safe_dossier_supports_non_execution_board(dossier_payload)
    return warnings

def non_execution_board_safety_flags_from_payload(payload: Dict[str, Any]) -> List[NonExecutionBoardRiskFlag]:
    flags = []
    # If the payload suggests active paper or mutation, flag it
    if payload.get("activation_allowed") is True:
        flags.append(NonExecutionBoardRiskFlag.ACTIVATION_ALLOWED_RISK)
    if payload.get("admission_allowed") is True:
        flags.append(NonExecutionBoardRiskFlag.ADMISSION_ALLOWED_RISK)
    if payload.get("transition_allowed") is True:
        flags.append(NonExecutionBoardRiskFlag.TRANSITION_ALLOWED_RISK)
    if payload.get("order_created") is True:
        flags.append(NonExecutionBoardRiskFlag.ORDER_CREATED_RISK)
    if payload.get("mutation_detected") is True:
        flags.append(NonExecutionBoardRiskFlag.MUTATION_DETECTED_RISK)

    for route in payload.get("runtime_route_items", []):
        if route.get("permission") == "ALLOWED" and route.get("dangerous", False):
            flags.append(NonExecutionBoardRiskFlag.DANGEROUS_RUNTIME_ROUTE_ALLOWED)
            break

    return flags

def non_execution_board_status_from_decision(decision: PaperReadinessNonExecutionBoardDecision) -> PaperReadinessNonExecutionBoardStatus:
    if decision == PaperReadinessNonExecutionBoardDecision.PASS_TO_NON_EXECUTION_BOARD_DOSSIER:
        return PaperReadinessNonExecutionBoardStatus.VALIDATED_NON_EXECUTION
    elif decision in [
        PaperReadinessNonExecutionBoardDecision.REQUEST_RUNTIME_MAP_REPLAY,
        PaperReadinessNonExecutionBoardDecision.REQUEST_SEAL_INTEGRITY_AUDIT,
        PaperReadinessNonExecutionBoardDecision.REQUEST_PAPER_SAFE_DOSSIER_REFRESH,
        PaperReadinessNonExecutionBoardDecision.REQUEST_MANUAL_REVIEW
    ]:
        return PaperReadinessNonExecutionBoardStatus.REQUEST_CHANGES
    elif decision == PaperReadinessNonExecutionBoardDecision.BLOCK:
        return PaperReadinessNonExecutionBoardStatus.BLOCKED
    elif decision == PaperReadinessNonExecutionBoardDecision.REJECT:
        return PaperReadinessNonExecutionBoardStatus.REJECTED
    return PaperReadinessNonExecutionBoardStatus.UNKNOWN

def eligibility_checker_to_text(payload: Dict[str, Any]) -> str:
    decision = evaluate_non_execution_board_eligibility(payload)
    reasons = non_execution_board_eligibility_reasons(payload)
    flags = non_execution_board_safety_flags_from_payload(payload)
    status = non_execution_board_status_from_decision(decision)

    lines = ["--- ELIGIBILITY CHECKER ---"]
    lines.append(f"Decision: {decision.value}")
    lines.append(f"Derived Status: {status.value}")
    if reasons:
        lines.append("Reasons:")
        for r in reasons:
            lines.append(f"  - {r}")
    if flags:
        lines.append("Risk Flags:")
        for f in flags:
            lines.append(f"  - {f.value}")
    return "\n".join(lines)
