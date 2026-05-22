from typing import Any
from usa_signal_bot.paper_readiness_confirmation.confirmation_models import (
    ReadinessConfirmationQueueItem,
    HumanReviewBundle,
    ActivationStillDeniedRegistryEntry,
    ReadinessConfirmationReview
)
from usa_signal_bot.paper_readiness_confirmation.confirmation_queue import build_readiness_confirmation_queue_item
from usa_signal_bot.paper_readiness_confirmation.human_review_bundle import build_human_review_bundle
from usa_signal_bot.paper_readiness_confirmation.activation_denied_registry import build_activation_still_denied_registry_entry
from usa_signal_bot.paper_readiness_confirmation.confirmation_report import build_readiness_confirmation_review

def confirmation_queue_from_firewall_audit(payload: dict[str, Any]) -> ReadinessConfirmationQueueItem:
    return build_readiness_confirmation_queue_item(payload)

def human_review_bundle_from_firewall_audit(payload: dict[str, Any]) -> HumanReviewBundle:
    queue_item = confirmation_queue_from_firewall_audit(payload)
    return build_human_review_bundle(queue_item)

def activation_denied_registry_from_firewall_audit(payload: dict[str, Any]) -> ActivationStillDeniedRegistryEntry:
    queue_item = confirmation_queue_from_firewall_audit(payload)
    bundle = build_human_review_bundle(queue_item)
    return build_activation_still_denied_registry_entry(queue_item, bundle)

def readiness_confirmation_review_from_firewall_audit(payload: dict[str, Any]) -> ReadinessConfirmationReview:
    queue_item = confirmation_queue_from_firewall_audit(payload)
    bundle = build_human_review_bundle(queue_item)
    registry_entry = build_activation_still_denied_registry_entry(queue_item, bundle)
    return build_readiness_confirmation_review(queue_item, bundle, registry_entry)

def attach_confirmation_metadata_to_firewall_audit_payload(payload: dict[str, Any], review: ReadinessConfirmationReview) -> dict[str, Any]:
    res = payload.copy()
    res["readiness_confirmation"] = {
        "review_id": review.review_id,
        "report_type": review.report_type.value
    }
    return res

def firewall_audit_confirmation_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"has_audit": bool(payload)}

def firewall_audit_adapter_to_text(payload: dict[str, Any]) -> str:
    return f"Firewall Audit Confirmation Summary: {firewall_audit_confirmation_summary(payload)}"
