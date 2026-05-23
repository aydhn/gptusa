from typing import Any
from datetime import datetime, timezone
import json
import hashlib
from usa_signal_bot.core.enums import (
    NoOrderSessionDossierStatus,
    NoOrderSessionDossierDecision,
    NoOrderDossierRiskFlag
)
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_models import (
    NoOrderPaperSessionDossier,
    create_no_order_dossier_id,
    NoOrderDossierEvidenceItem,
    BridgeReplayAuditSeal,
    PaperAdmissionBlockerEvent,
    no_order_paper_session_dossier_to_dict
)
from usa_signal_bot.paper_no_order_dossier.bridge_ingestion import (
    extract_no_order_session,
    extract_bridge_dry_run,
    extract_bridge_replay_result
)

def stable_no_order_dossier_hash(payload: dict[str, Any]) -> str:
    s = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def collect_no_order_dossier_safety_flags(bridge_payload: dict[str, Any], evidence_items: list[NoOrderDossierEvidenceItem]) -> list[NoOrderDossierRiskFlag]:
    flags = []

    if bridge_payload.get("activation_allowed"):
        flags.append(NoOrderDossierRiskFlag.ACTIVATION_ALLOWED_RISK)
    if bridge_payload.get("transition_allowed"):
        flags.append(NoOrderDossierRiskFlag.TRANSITION_ALLOWED_RISK)
    if bridge_payload.get("order_created"):
        flags.append(NoOrderDossierRiskFlag.ORDER_CREATED_RISK)
    if bridge_payload.get("mutation_detected"):
        flags.append(NoOrderDossierRiskFlag.MUTATION_DETECTED_RISK)

    session = extract_no_order_session(bridge_payload)
    if session and session.get("status") in ["FAILED", "ERROR"]:
        flags.append(NoOrderDossierRiskFlag.NO_ORDER_SESSION_FAILED)

    for item in evidence_items:
        if item.required and not item.available:
            flags.append(NoOrderDossierRiskFlag.DOSSIER_EVIDENCE_MISSING)
        if item.required and item.stale:
            flags.append(NoOrderDossierRiskFlag.DOSSIER_EVIDENCE_STALE)

    return list(set(flags))

def build_default_no_order_dossier(candidate_id: str | None = None) -> NoOrderPaperSessionDossier:
    return NoOrderPaperSessionDossier(
        dossier_id=create_no_order_dossier_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=NoOrderSessionDossierStatus.DRAFT,
        decision=NoOrderSessionDossierDecision.UNKNOWN,
        candidate_id=candidate_id,
        source_bridge_review_id=None,
        source_bridge_dry_run_id=None,
        source_no_order_session_id=None,
        source_bridge_replay_result_id=None,
        evidence_items=[],
        bridge_replay_audit_seal=None,
        blocker_events=[],
        evidence_refs=[],
        dossier_hash=None,
        sealed=False,
        immutable=False,
        manual_review_required=True,
        activation_denied=True,
        activation_allowed=False,
        admission_allowed=False,
        transition_allowed=False,
        all_writes_blocked=True,
        order_created=False,
        mutation_detected=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        safety_flags=[],
        required_followups=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def build_no_order_paper_session_dossier(bridge_payload: dict[str, Any]) -> NoOrderPaperSessionDossier:
    from usa_signal_bot.paper_no_order_dossier.dossier_evidence import collect_no_order_dossier_evidence
    from usa_signal_bot.paper_no_order_dossier.bridge_replay_audit_seal import build_bridge_replay_audit_seal
    from usa_signal_bot.paper_no_order_dossier.admission_attempt_simulator import simulate_paper_admission_attempts

    evidence = collect_no_order_dossier_evidence(bridge_payload)
    seal = build_bridge_replay_audit_seal(bridge_payload, evidence)
    blocker_events = simulate_paper_admission_attempts()

    flags = collect_no_order_dossier_safety_flags(bridge_payload, evidence)

    # Needs a valid status based on the flags/bridge payload, simplified logic for builder:
    has_blocking_flags = any(f for f in flags if f not in [NoOrderDossierRiskFlag.DOSSIER_EVIDENCE_MISSING])
    status = NoOrderSessionDossierStatus.BLOCKED if has_blocking_flags else NoOrderSessionDossierStatus.VALIDATED_NO_ORDER
    decision = NoOrderSessionDossierDecision.BLOCK if has_blocking_flags else NoOrderSessionDossierDecision.CREATE_NO_ORDER_SESSION_DOSSIER

    session = extract_no_order_session(bridge_payload)
    dry_run = extract_bridge_dry_run(bridge_payload)
    replay = extract_bridge_replay_result(bridge_payload)

    dossier = NoOrderPaperSessionDossier(
        dossier_id=create_no_order_dossier_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=status,
        decision=decision,
        candidate_id=bridge_payload.get("candidate_id"),
        source_bridge_review_id=bridge_payload.get("review_id"),
        source_bridge_dry_run_id=dry_run.get("dry_run_id") if dry_run else None,
        source_no_order_session_id=session.get("session_id") if session else None,
        source_bridge_replay_result_id=replay.get("replay_id") if replay else None,
        evidence_items=evidence,
        bridge_replay_audit_seal=seal,
        blocker_events=blocker_events,
        evidence_refs=[e.evidence_id for e in evidence],
        dossier_hash=None, # Set below
        sealed=True,
        immutable=True,
        manual_review_required=True,
        activation_denied=True,
        activation_allowed=False,
        admission_allowed=False,
        transition_allowed=False,
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
        metadata={}
    )

    dossier.dossier_hash = stable_no_order_dossier_hash(no_order_paper_session_dossier_to_dict(dossier))
    return dossier

def no_order_dossier_summary(dossier: NoOrderPaperSessionDossier) -> dict[str, Any]:
    return {
        "dossier_id": dossier.dossier_id,
        "status": dossier.status,
        "decision": dossier.decision,
        "sealed": dossier.sealed,
        "evidence_count": len(dossier.evidence_items),
        "safety_flag_count": len(dossier.safety_flags)
    }

def no_order_dossier_to_text(dossier: NoOrderPaperSessionDossier, limit: int = 100) -> str:
    return json.dumps(no_order_dossier_summary(dossier), indent=2)
