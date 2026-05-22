from typing import Any
import datetime

from usa_signal_bot.paper_readiness_confirmation.confirmation_models import (
    ReadinessConfirmationQueueItem,
    create_readiness_confirmation_queue_item_id
)
from usa_signal_bot.core.enums import ReadinessConfirmationQueueStatus, ReadinessConfirmationDecision, ReadinessConfidenceLevel
from usa_signal_bot.paper_readiness_confirmation.eligibility_checker import (
    evaluate_readiness_confirmation_eligibility,
    readiness_confirmation_status_from_decision,
    readiness_confirmation_safety_flags_from_firewall_audit
)
from usa_signal_bot.paper_readiness_confirmation.readiness_confidence import calculate_readiness_confidence
from usa_signal_bot.paper_readiness_confirmation.firewall_audit_ingestion import (
    extract_readiness_audit_checkpoint,
    extract_firewall_replay_result,
    extract_zero_mutation_audit,
    extract_firewall_audit_candidate_id
)

def build_readiness_confirmation_queue_item(firewall_audit_payload: dict[str, Any]) -> ReadinessConfirmationQueueItem:
    decision = evaluate_readiness_confirmation_eligibility(firewall_audit_payload)
    status = readiness_confirmation_status_from_decision(decision)
    confidence = calculate_readiness_confidence(firewall_audit_payload)
    flags = readiness_confirmation_safety_flags_from_firewall_audit(firewall_audit_payload)

    zero_audit = extract_zero_mutation_audit(firewall_audit_payload)
    replay = extract_firewall_replay_result(firewall_audit_payload)
    checkpoint = extract_readiness_audit_checkpoint(firewall_audit_payload)

    return ReadinessConfirmationQueueItem(
        queue_item_id=create_readiness_confirmation_queue_item_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        status=status,
        decision=decision,
        candidate_id=extract_firewall_audit_candidate_id(firewall_audit_payload),
        source_firewall_audit_review_id=firewall_audit_payload.get("review_id"),
        source_readiness_audit_checkpoint_id=checkpoint.get("checkpoint_id") if checkpoint else None,
        source_zero_mutation_audit_id=zero_audit.get("audit_id") if zero_audit else None,
        source_firewall_replay_result_id=replay.get("replay_id") if replay else None,
        evidence_refs=[],
        required_followups=[],
        readiness_confidence=confidence,
        safety_flags=flags,
        manual_review_required=True,
        activation_denied_required=True,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        warnings=[],
        errors=[]
    )

def build_default_confirmation_queue_item(candidate_id: str | None = None) -> ReadinessConfirmationQueueItem:
    return ReadinessConfirmationQueueItem(
        queue_item_id=create_readiness_confirmation_queue_item_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        status=ReadinessConfirmationQueueStatus.DRAFT,
        decision=ReadinessConfirmationDecision.UNKNOWN,
        candidate_id=candidate_id,
        source_firewall_audit_review_id=None,
        source_readiness_audit_checkpoint_id=None,
        source_zero_mutation_audit_id=None,
        source_firewall_replay_result_id=None,
        evidence_refs=[],
        required_followups=[],
        readiness_confidence=ReadinessConfidenceLevel.UNKNOWN,
        safety_flags=[],
        manual_review_required=True,
        activation_denied_required=True,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        warnings=[],
        errors=[]
    )

def validate_confirmation_queue_item_safety(item: ReadinessConfirmationQueueItem) -> list[str]:
    errors = []
    if not item.activation_denied_required:
        errors.append("activation_denied_required must be True")
    if not item.manual_review_required:
        errors.append("manual_review_required must be True")
    if item.allows_active_paper:
         errors.append("allows_active_paper must be False")
    if item.allows_broker_execution:
         errors.append("allows_broker_execution must be False")
    if item.allows_paper_state_mutation:
         errors.append("allows_paper_state_mutation must be False")
    if item.allows_config_patch:
         errors.append("allows_config_patch must be False")
    if item.allows_telegram_real_send:
         errors.append("allows_telegram_real_send must be False")
    return errors

def confirmation_queue_item_summary(item: ReadinessConfirmationQueueItem) -> dict[str, Any]:
    return {
        "queue_item_id": item.queue_item_id,
        "status": item.status.value,
        "decision": item.decision.value,
        "candidate_id": item.candidate_id,
        "confidence": item.readiness_confidence.value,
        "safety_flags": [f.value for f in item.safety_flags]
    }

def confirmation_queue_item_to_text(item: ReadinessConfirmationQueueItem) -> str:
    summary = confirmation_queue_item_summary(item)
    return f"Queue Item: {summary['queue_item_id']}, Status: {summary['status']}, Decision: {summary['decision']}"
