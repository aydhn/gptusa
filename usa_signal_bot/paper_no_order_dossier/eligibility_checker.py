from typing import Any
import json
from usa_signal_bot.core.enums import (
    NoOrderSessionDossierDecision,
    NoOrderSessionDossierStatus,
    NoOrderDossierRiskFlag
)
from usa_signal_bot.paper_no_order_dossier.bridge_ingestion import (
    bridge_review_supports_no_order_dossier,
    extract_no_order_session,
    extract_bridge_replay_result
)

def evaluate_no_order_dossier_eligibility(bridge_payload: dict[str, Any]) -> NoOrderSessionDossierDecision:
    supports, reasons = bridge_review_supports_no_order_dossier(bridge_payload)
    if not supports:
        if any("allowed is true" in r or "created is true" in r or "detected is true" in r for r in reasons):
            return NoOrderSessionDossierDecision.BLOCK
        if any("no_order_session" in r for r in reasons):
            return NoOrderSessionDossierDecision.REQUEST_NO_ORDER_SESSION_REFRESH
        if any("bridge_replay_result" in r for r in reasons):
            return NoOrderSessionDossierDecision.REQUEST_BRIDGE_REPLAY_REFRESH
        return NoOrderSessionDossierDecision.REQUEST_BRIDGE_REVIEW_REFRESH

    return NoOrderSessionDossierDecision.CREATE_NO_ORDER_SESSION_DOSSIER

def no_order_dossier_eligibility_reasons(bridge_payload: dict[str, Any]) -> list[str]:
    _, reasons = bridge_review_supports_no_order_dossier(bridge_payload)
    return reasons

def no_order_dossier_safety_flags_from_bridge(payload: dict[str, Any]) -> list[NoOrderDossierRiskFlag]:
    flags = []
    if payload.get("activation_allowed"):
        flags.append(NoOrderDossierRiskFlag.ACTIVATION_ALLOWED_RISK)
    if payload.get("transition_allowed"):
        flags.append(NoOrderDossierRiskFlag.TRANSITION_ALLOWED_RISK)
    if payload.get("order_created"):
        flags.append(NoOrderDossierRiskFlag.ORDER_CREATED_RISK)
    if payload.get("mutation_detected"):
        flags.append(NoOrderDossierRiskFlag.MUTATION_DETECTED_RISK)
    if payload.get("dangerous_allowed_count", 0) > 0:
        flags.append(NoOrderDossierRiskFlag.DANGEROUS_ROUTE_ALLOWED)

    session = extract_no_order_session(payload)
    if session and session.get("status") in ["FAILED", "ERROR"]:
        flags.append(NoOrderDossierRiskFlag.NO_ORDER_SESSION_FAILED)

    replay = extract_bridge_replay_result(payload)
    if replay and replay.get("status") in ["FAILED", "ERROR"]:
        flags.append(NoOrderDossierRiskFlag.BRIDGE_REPLAY_FAILED)

    return flags

def no_order_dossier_status_from_decision(decision: NoOrderSessionDossierDecision) -> NoOrderSessionDossierStatus:
    if decision == NoOrderSessionDossierDecision.CREATE_NO_ORDER_SESSION_DOSSIER:
        return NoOrderSessionDossierStatus.VALIDATED_NO_ORDER
    if decision in [NoOrderSessionDossierDecision.BLOCK, NoOrderSessionDossierDecision.REJECT]:
        return NoOrderSessionDossierStatus.BLOCKED
    if decision in [
        NoOrderSessionDossierDecision.REQUEST_BRIDGE_REVIEW_REFRESH,
        NoOrderSessionDossierDecision.REQUEST_NO_ORDER_SESSION_REFRESH,
        NoOrderSessionDossierDecision.REQUEST_BRIDGE_REPLAY_REFRESH,
        NoOrderSessionDossierDecision.REQUEST_MANUAL_REVIEW
    ]:
        return NoOrderSessionDossierStatus.REQUEST_CHANGES
    return NoOrderSessionDossierStatus.UNKNOWN

def eligibility_checker_to_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)
