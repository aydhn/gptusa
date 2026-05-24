from typing import Any
from usa_signal_bot.core.enums import (
    PaperReadinessBoardDossierDecision,
    PaperReadinessBoardDossierStatus,
    BoardDossierRiskFlag
)
from usa_signal_bot.paper_readiness_board_dossier.non_execution_board_ingestion import (
    extract_non_execution_board,
    extract_runtime_map_replay_result,
    extract_non_execution_seal_integrity_audit,
    extract_board_decision
)

def evaluate_board_dossier_eligibility(board_payload: dict[str, Any]) -> PaperReadinessBoardDossierDecision:
    flags = board_dossier_safety_flags_from_payload(board_payload)
    if flags:
        if BoardDossierRiskFlag.SECRET_RISK in flags:
            return PaperReadinessBoardDossierDecision.BLOCK
        return PaperReadinessBoardDossierDecision.BLOCK

    board = extract_non_execution_board(board_payload)
    if not board:
        return PaperReadinessBoardDossierDecision.REQUEST_NON_EXECUTION_BOARD_REFRESH

    decision = extract_board_decision(board_payload)
    if decision in ["PASS_TO_NON_EXECUTION_BOARD_DOSSIER", "VALIDATED_NON_EXECUTION"]:
        replay = extract_runtime_map_replay_result(board_payload)
        seal = extract_non_execution_seal_integrity_audit(board_payload)

        if replay and replay.get("status") == "COMPLETED_ROUTE_SAFE" and seal and seal.get("status") == "VALIDATED":
            return PaperReadinessBoardDossierDecision.CREATE_BOARD_DOSSIER

    if decision == "REJECT":
        return PaperReadinessBoardDossierDecision.REJECT

    return PaperReadinessBoardDossierDecision.INCONCLUSIVE

def board_dossier_eligibility_reasons(board_payload: dict[str, Any]) -> list[str]:
    reasons = []
    board = extract_non_execution_board(board_payload)
    if not board:
        reasons.append("Missing non_execution_board")
    else:
        decision = extract_board_decision(board_payload)
        if decision not in ["PASS_TO_NON_EXECUTION_BOARD_DOSSIER", "VALIDATED_NON_EXECUTION"]:
            reasons.append(f"Non-execution board decision is not PASS: {decision}")

    replay = extract_runtime_map_replay_result(board_payload)
    if not replay:
        reasons.append("Missing runtime_map_replay_result")
    elif replay.get("status") != "COMPLETED_ROUTE_SAFE":
        reasons.append("Runtime map replay not safe")

    seal = extract_non_execution_seal_integrity_audit(board_payload)
    if not seal:
        reasons.append("Missing seal_integrity_audit")
    elif seal.get("status") != "VALIDATED":
        reasons.append("Seal integrity audit not validated")

    return reasons

def board_dossier_safety_flags_from_payload(payload: dict[str, Any]) -> list[BoardDossierRiskFlag]:
    flags = []
    board = extract_non_execution_board(payload)
    if board:
        if board.get("activation_allowed") is True:
            flags.append(BoardDossierRiskFlag.ACTIVATION_ALLOWED_RISK)
        if board.get("admission_allowed") is True:
            flags.append(BoardDossierRiskFlag.ADMISSION_ALLOWED_RISK)
        if board.get("transition_allowed") is True:
            flags.append(BoardDossierRiskFlag.TRANSITION_ALLOWED_RISK)
        if board.get("order_created") is True:
            flags.append(BoardDossierRiskFlag.ORDER_CREATED_RISK)
        if board.get("mutation_detected") is True:
            flags.append(BoardDossierRiskFlag.MUTATION_DETECTED_RISK)

    replay = extract_runtime_map_replay_result(payload)
    if replay and replay.get("all_dangerous_routes_denied") is False:
        flags.append(BoardDossierRiskFlag.RUNTIME_MAP_REPLAY_FAILED)

    seal = extract_non_execution_seal_integrity_audit(payload)
    if seal and seal.get("seal_hash_matches") is False:
        flags.append(BoardDossierRiskFlag.NON_EXECUTION_SEAL_INTEGRITY_FAILED)

    return flags

def board_dossier_status_from_decision(decision: PaperReadinessBoardDossierDecision) -> PaperReadinessBoardDossierStatus:
    if decision == PaperReadinessBoardDossierDecision.CREATE_BOARD_DOSSIER:
        return PaperReadinessBoardDossierStatus.VALIDATED_NON_EXECUTION
    if decision == PaperReadinessBoardDossierDecision.BLOCK:
        return PaperReadinessBoardDossierStatus.BLOCKED
    if decision == PaperReadinessBoardDossierDecision.REJECT:
        return PaperReadinessBoardDossierStatus.REJECTED
    return PaperReadinessBoardDossierStatus.REQUEST_CHANGES

def eligibility_checker_to_text(payload: dict[str, Any]) -> str:
    decision = evaluate_board_dossier_eligibility(payload)
    reasons = board_dossier_eligibility_reasons(payload)
    flags = board_dossier_safety_flags_from_payload(payload)

    parts = [f"Decision: {decision.name}"]
    if reasons:
        parts.append("Reasons:")
        for r in reasons:
            parts.append(f"  - {r}")
    if flags:
        parts.append("Risk Flags:")
        for f in flags:
            parts.append(f"  - {f.name}")
    return "\n".join(parts)
