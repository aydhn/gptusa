from typing import Any
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    PaperReadinessBoardDossierStatus,
    PaperReadinessBoardDossierDecision,
    BoardDossierRiskFlag
)
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_models import (
    PaperReadinessBoardDossier,
    BoardDossierEvidenceItem,
    AcceptanceBoardSeal,
    ShadowLaunchBlockerEvent,
    create_board_dossier_id
)
from usa_signal_bot.paper_readiness_board_dossier.eligibility_checker import (
    evaluate_board_dossier_eligibility,
    board_dossier_status_from_decision
)
from usa_signal_bot.paper_readiness_board_dossier.dossier_evidence import collect_board_dossier_evidence
from usa_signal_bot.paper_readiness_board_dossier.acceptance_board_seal import build_acceptance_board_seal
from usa_signal_bot.paper_readiness_board_dossier.shadow_launch_attempt_simulator import simulate_shadow_launch_attempts
from usa_signal_bot.paper_readiness_board_dossier.non_execution_board_ingestion import (
    extract_non_execution_board,
    extract_board_candidate_id,
    extract_runtime_map_replay_result,
    extract_non_execution_seal_integrity_audit
)

def collect_board_dossier_safety_flags(board_payload: dict[str, Any], evidence_items: list[BoardDossierEvidenceItem]) -> list[BoardDossierRiskFlag]:
    flags = []

    board = extract_non_execution_board(board_payload)
    if not board or board.get("decision") not in ["PASS_TO_NON_EXECUTION_BOARD_DOSSIER", "VALIDATED_NON_EXECUTION"]:
        flags.append(BoardDossierRiskFlag.NON_EXECUTION_BOARD_FAILED)

    missing_required = any(e.required and not e.available for e in evidence_items)
    if missing_required:
        flags.append(BoardDossierRiskFlag.DOSSIER_EVIDENCE_MISSING)

    return flags

def stable_board_dossier_hash(payload: dict[str, Any]) -> str:
    import hashlib
    import json
    serialized = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

def build_paper_readiness_board_dossier(board_payload: dict[str, Any]) -> PaperReadinessBoardDossier:
    decision = evaluate_board_dossier_eligibility(board_payload)
    status = board_dossier_status_from_decision(decision)

    evidence_items = collect_board_dossier_evidence(board_payload)
    seal = build_acceptance_board_seal(board_payload, evidence_items)
    blocker_events = simulate_shadow_launch_attempts()

    flags = collect_board_dossier_safety_flags(board_payload, evidence_items)

    board = extract_non_execution_board(board_payload)
    replay = extract_runtime_map_replay_result(board_payload)
    audit = extract_non_execution_seal_integrity_audit(board_payload)

    valid_board = board is not None and board.get("decision") in ["PASS_TO_NON_EXECUTION_BOARD_DOSSIER", "VALIDATED_NON_EXECUTION"]
    valid_replay = replay is not None and replay.get("status") == "COMPLETED_ROUTE_SAFE"
    valid_audit = audit is not None and audit.get("status") == "VALIDATED"

    return PaperReadinessBoardDossier(
        dossier_id=create_board_dossier_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=status,
        decision=decision,
        evidence_items=evidence_items,
        shadow_launch_blocker_events=blocker_events,
        evidence_refs=[e.evidence_id for e in evidence_items if e.available],
        sealed=True,
        immutable=True,
        manual_review_required=True,
        activation_denied=True,
        activation_allowed=False,
        admission_allowed=False,
        transition_allowed=False,
        shadow_launch_allowed=False,
        paper_mode_launch_allowed=False,
        paper_safe_dossier_valid=True,
        non_execution_board_valid=valid_board,
        non_execution_confirmed=valid_board,
        runtime_map_safe=valid_replay,
        all_writes_blocked=True,
        order_created=False,
        mutation_detected=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        safety_flags=flags,
        required_followups=[],
        warnings=[],
        errors=[],
        acceptance_board_seal=seal,
        candidate_id=extract_board_candidate_id(board_payload),
        source_non_execution_board_review_id=board_payload.get("review_id"),
        source_non_execution_board_id=board.get("board_id") if board else None,
        source_runtime_replay_result_id=replay.get("result_id") if replay else None,
        source_seal_integrity_audit_id=audit.get("audit_id") if audit else None,
        dossier_hash=stable_board_dossier_hash(board_payload)
    )

def build_default_board_dossier(candidate_id: str | None = None) -> PaperReadinessBoardDossier:
    return PaperReadinessBoardDossier(
        dossier_id=create_board_dossier_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=PaperReadinessBoardDossierStatus.FAILED,
        decision=PaperReadinessBoardDossierDecision.BLOCK,
        evidence_items=[],
        shadow_launch_blocker_events=[],
        evidence_refs=[],
        sealed=True,
        immutable=True,
        manual_review_required=True,
        activation_denied=True,
        activation_allowed=False,
        admission_allowed=False,
        transition_allowed=False,
        shadow_launch_allowed=False,
        paper_mode_launch_allowed=False,
        paper_safe_dossier_valid=False,
        non_execution_board_valid=False,
        non_execution_confirmed=False,
        runtime_map_safe=False,
        all_writes_blocked=True,
        order_created=False,
        mutation_detected=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        safety_flags=[BoardDossierRiskFlag.NON_EXECUTION_BOARD_FAILED],
        required_followups=["Manual review required"],
        warnings=["Created default failing dossier"],
        errors=["Missing board payload"],
        candidate_id=candidate_id
    )

def board_dossier_summary(dossier: PaperReadinessBoardDossier) -> dict[str, Any]:
    return {
        "status": dossier.status.name,
        "decision": dossier.decision.name,
        "sealed": dossier.sealed,
        "non_execution_board_valid": dossier.non_execution_board_valid,
        "all_writes_blocked": dossier.all_writes_blocked,
        "has_seal": dossier.acceptance_board_seal is not None,
        "blocker_event_count": len(dossier.shadow_launch_blocker_events)
    }

def board_dossier_to_text(dossier: PaperReadinessBoardDossier, limit: int = 100) -> str:
    lines = [
        f"Board Dossier ({dossier.dossier_id}):",
        f"  Status: {dossier.status.name}",
        f"  Decision: {dossier.decision.name}",
        f"  Candidate ID: {dossier.candidate_id or 'N/A'}",
        f"  Sealed: {dossier.sealed}",
        f"  All Writes Blocked: {dossier.all_writes_blocked}",
        f"  Allows Execution/Launch: False (GUARANTEED)"
    ]
    return "\n".join(lines)
