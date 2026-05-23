from typing import Any
import json
import hashlib
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    BridgeReplayAuditSealStatus,
    BridgeReplayAuditSealDecision,
    NoOrderDossierRiskFlag
)
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_models import (
    BridgeReplayAuditSeal,
    create_bridge_replay_audit_seal_id,
    NoOrderDossierEvidenceItem,
    bridge_replay_audit_seal_to_dict
)
from usa_signal_bot.paper_no_order_dossier.bridge_ingestion import (
    extract_bridge_replay_result,
    extract_bridge_route_attempts
)

def stable_bridge_replay_hash(payload: dict[str, Any]) -> str:
    s = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def stable_route_attempt_hash(attempts: list[dict[str, Any]]) -> str:
    s = json.dumps(attempts, sort_keys=True)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def stable_dangerous_route_coverage_hash(payload: dict[str, Any]) -> str:
    s = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def collect_bridge_replay_seal_risk_flags(bridge_payload: dict[str, Any]) -> list[NoOrderDossierRiskFlag]:
    flags = []
    replay = extract_bridge_replay_result(bridge_payload)
    if not replay:
        flags.append(NoOrderDossierRiskFlag.BRIDGE_REPLAY_FAILED)
    elif replay.get("status") in ["FAILED", "ERROR"]:
        flags.append(NoOrderDossierRiskFlag.BRIDGE_REPLAY_FAILED)

    if bridge_payload.get("dangerous_allowed_count", 0) > 0:
        flags.append(NoOrderDossierRiskFlag.DANGEROUS_ROUTE_ALLOWED)

    return flags

def build_bridge_replay_audit_seal(bridge_payload: dict[str, Any], evidence_items: list[NoOrderDossierEvidenceItem] | None = None) -> BridgeReplayAuditSeal:
    replay = extract_bridge_replay_result(bridge_payload) or {}
    attempts = extract_bridge_route_attempts(bridge_payload)

    dangerous_allowed = bridge_payload.get("dangerous_allowed_count", 0)
    all_denied = (dangerous_allowed == 0)

    replay_passed = (replay.get("status") not in ["FAILED", "ERROR"] and all_denied)

    status = BridgeReplayAuditSealStatus.SEALED if replay_passed else BridgeReplayAuditSealStatus.FAILED
    decision = BridgeReplayAuditSealDecision.SEAL_BRIDGE_REPLAY_AUDIT if replay_passed else BridgeReplayAuditSealDecision.BLOCK

    return BridgeReplayAuditSeal(
        seal_id=create_bridge_replay_audit_seal_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=status,
        decision=decision,
        candidate_id=bridge_payload.get("candidate_id"),
        source_bridge_replay_result_id=replay.get("replay_id"),
        source_bridge_review_id=bridge_payload.get("review_id"),
        replay_hash=stable_bridge_replay_hash(replay),
        route_attempt_hash=stable_route_attempt_hash(attempts),
        dangerous_route_coverage_hash=stable_dangerous_route_coverage_hash(bridge_payload.get("dangerous_route_coverage", {})),
        sealed=True,
        immutable=True,
        replay_passed=replay_passed,
        all_dangerous_routes_denied=all_denied,
        dangerous_allowed_count=dangerous_allowed,
        read_only_allowed_count=bridge_payload.get("read_only_allowed_count", 0),
        missing_route_count=bridge_payload.get("missing_route_count", 0),
        evidence_refs=[e.evidence_id for e in evidence_items] if evidence_items else [],
        risk_flags=collect_bridge_replay_seal_risk_flags(bridge_payload),
        required_followups=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def bridge_replay_audit_seal_summary(seal: BridgeReplayAuditSeal) -> dict[str, Any]:
    return {
        "seal_id": seal.seal_id,
        "status": seal.status,
        "decision": seal.decision,
        "sealed": seal.sealed,
        "replay_passed": seal.replay_passed
    }

def bridge_replay_audit_seal_to_text(seal: BridgeReplayAuditSeal) -> str:
    return json.dumps(bridge_replay_audit_seal_to_dict(seal), indent=2)
