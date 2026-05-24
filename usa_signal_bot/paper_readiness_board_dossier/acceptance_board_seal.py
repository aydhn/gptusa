from typing import Any
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    AcceptanceBoardSealStatus,
    AcceptanceBoardSealDecision,
    BoardDossierRiskFlag
)
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_models import (
    AcceptanceBoardSeal,
    BoardDossierEvidenceItem,
    create_acceptance_board_seal_id
)
from usa_signal_bot.paper_readiness_board_dossier.non_execution_board_ingestion import (
    extract_non_execution_board,
    extract_runtime_map_replay_result,
    extract_non_execution_seal_integrity_audit,
    extract_board_candidate_id
)

def accepted_board_boundaries() -> list[str]:
    return [
        "non_execution_board_valid",
        "runtime_map_replay_passed",
        "all_dangerous_runtime_routes_denied",
        "non_execution_seal_integrity_valid",
        "board_gates_passed",
        "board_assertions_passed",
        "no_shadow_launch_permission",
        "no_paper_mode_launch_permission",
        "no_active_paper_permission",
        "not_investment_advice"
    ]

def build_acceptance_board_seal(board_payload: dict[str, Any], evidence_items: list[BoardDossierEvidenceItem] | None = None) -> AcceptanceBoardSeal:
    board = extract_non_execution_board(board_payload)
    replay = extract_runtime_map_replay_result(board_payload)
    seal = extract_non_execution_seal_integrity_audit(board_payload)

    board_valid = board is not None and board.get("decision") in ["PASS_TO_NON_EXECUTION_BOARD_DOSSIER", "VALIDATED_NON_EXECUTION"]
    replay_valid = replay is not None and replay.get("status") == "COMPLETED_ROUTE_SAFE"
    all_denied = replay is not None and replay.get("all_dangerous_routes_denied") is True
    seal_valid = seal is not None and seal.get("status") == "VALIDATED"

    status = AcceptanceBoardSealStatus.SEALED if (board_valid and replay_valid and all_denied and seal_valid) else AcceptanceBoardSealStatus.FAILED
    decision = AcceptanceBoardSealDecision.SEAL_ACCEPTANCE_BOARD if status == AcceptanceBoardSealStatus.SEALED else AcceptanceBoardSealDecision.BLOCK

    return AcceptanceBoardSeal(
        seal_id=create_acceptance_board_seal_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=status,
        decision=decision,
        board_gates_passed=board_valid,
        board_assertions_passed=board_valid,
        runtime_replay_passed=replay_valid,
        all_dangerous_runtime_routes_denied=all_denied,
        non_execution_seal_integrity_valid=seal_valid,
        sealed=True,
        immutable=True,
        seal_is_metadata_only=True,
        allows_shadow_launch=False,
        allows_paper_mode_launch=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        risk_flags=collect_acceptance_board_seal_risk_flags(board_payload),
        required_followups=[],
        warnings=[],
        errors=[],
        accepted_boundaries=accepted_board_boundaries(),
        candidate_id=extract_board_candidate_id(board_payload),
        source_board_id=board.get("board_id") if board else None,
        source_runtime_replay_result_id=replay.get("result_id") if replay else None,
        source_seal_integrity_audit_id=seal.get("audit_id") if seal else None,
        seal_hash=stable_acceptance_board_seal_hash(board_payload)
    )

def build_default_acceptance_board_seal(candidate_id: str | None = None) -> AcceptanceBoardSeal:
    return AcceptanceBoardSeal(
        seal_id=create_acceptance_board_seal_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=AcceptanceBoardSealStatus.FAILED,
        decision=AcceptanceBoardSealDecision.BLOCK,
        board_gates_passed=False,
        board_assertions_passed=False,
        runtime_replay_passed=False,
        all_dangerous_runtime_routes_denied=False,
        non_execution_seal_integrity_valid=False,
        sealed=True,
        immutable=True,
        seal_is_metadata_only=True,
        allows_shadow_launch=False,
        allows_paper_mode_launch=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        risk_flags=[BoardDossierRiskFlag.ACCEPTANCE_BOARD_SEAL_FAILED],
        required_followups=["Manual review required"],
        warnings=["Created default failing seal"],
        errors=["Missing board payload"],
        accepted_boundaries=accepted_board_boundaries(),
        candidate_id=candidate_id
    )

def stable_acceptance_board_seal_hash(payload: dict[str, Any]) -> str:
    import hashlib
    import json
    # A simple stable hash representation
    serialized = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

def collect_acceptance_board_seal_risk_flags(board_payload: dict[str, Any]) -> list[BoardDossierRiskFlag]:
    flags = []
    board = extract_non_execution_board(board_payload)
    if not board or board.get("decision") not in ["PASS_TO_NON_EXECUTION_BOARD_DOSSIER", "VALIDATED_NON_EXECUTION"]:
        flags.append(BoardDossierRiskFlag.NON_EXECUTION_BOARD_FAILED)

    replay = extract_runtime_map_replay_result(board_payload)
    if not replay or replay.get("status") != "COMPLETED_ROUTE_SAFE":
        flags.append(BoardDossierRiskFlag.RUNTIME_MAP_REPLAY_FAILED)

    seal = extract_non_execution_seal_integrity_audit(board_payload)
    if not seal or seal.get("status") != "VALIDATED":
        flags.append(BoardDossierRiskFlag.NON_EXECUTION_SEAL_INTEGRITY_FAILED)

    return flags

def acceptance_board_seal_summary(seal: AcceptanceBoardSeal) -> dict[str, Any]:
    return {
        "status": seal.status.name,
        "decision": seal.decision.name,
        "sealed": seal.sealed,
        "immutable": seal.immutable,
        "board_gates_passed": seal.board_gates_passed,
        "board_assertions_passed": seal.board_assertions_passed,
        "runtime_replay_passed": seal.runtime_replay_passed,
        "non_execution_seal_integrity_valid": seal.non_execution_seal_integrity_valid,
        "all_dangerous_runtime_routes_denied": seal.all_dangerous_runtime_routes_denied
    }

def acceptance_board_seal_to_text(seal: AcceptanceBoardSeal) -> str:
    lines = [
        f"Acceptance Board Seal ({seal.seal_id}):",
        f"  Status: {seal.status.name}",
        f"  Decision: {seal.decision.name}",
        f"  Candidate ID: {seal.candidate_id or 'N/A'}",
        f"  Board Gates Passed: {seal.board_gates_passed}",
        f"  Runtime Replay Passed: {seal.runtime_replay_passed}",
        f"  Seal Integrity Valid: {seal.non_execution_seal_integrity_valid}",
        f"  Allows Execution/Launch: False (GUARANTEED)"
    ]
    return "\n".join(lines)
