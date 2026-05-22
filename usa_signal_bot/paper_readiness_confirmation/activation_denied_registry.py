from typing import Any
import datetime

from usa_signal_bot.paper_readiness_confirmation.confirmation_models import (
    ActivationStillDeniedRegistryEntry,
    ReadinessConfirmationQueueItem,
    HumanReviewBundle,
    create_activation_still_denied_registry_entry_id
)
from usa_signal_bot.core.enums import ActivationStillDeniedRegistryStatus, ActivationStillDeniedDecision

def build_activation_still_denied_registry_entry(
    queue_item: ReadinessConfirmationQueueItem,
    bundle: HumanReviewBundle | None = None
) -> ActivationStillDeniedRegistryEntry:

    return ActivationStillDeniedRegistryEntry(
        registry_entry_id=create_activation_still_denied_registry_entry_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        status=ActivationStillDeniedRegistryStatus.DRAFT,
        decision=ActivationStillDeniedDecision.UNKNOWN,
        candidate_id=queue_item.candidate_id,
        queue_item_id=queue_item.queue_item_id,
        bundle_id=bundle.bundle_id if bundle else None,
        source_checkpoint_id=queue_item.source_readiness_audit_checkpoint_id,
        activation_denied=True,
        activation_allowed=False,
        denial_reason="Activation strictly denied by Readiness Confirmation layer.",
        required_followups=list(queue_item.required_followups),
        safety_flags=list(queue_item.safety_flags),
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        warnings=[],
        errors=[],
        metadata={}
    )

def register_activation_still_denied_entry(
    entry: ActivationStillDeniedRegistryEntry,
    registry: list[ActivationStillDeniedRegistryEntry] | None = None
) -> list[ActivationStillDeniedRegistryEntry]:
    reg = registry or []
    if entry.activation_allowed or not entry.activation_denied:
         entry.errors.append("Cannot register entry: activation not denied.")
         entry.status = ActivationStillDeniedRegistryStatus.BLOCKED
    else:
         entry.status = ActivationStillDeniedRegistryStatus.REGISTERED
    reg.append(entry)
    return reg

def find_activation_denied_entry_by_id(
    registry: list[ActivationStillDeniedRegistryEntry],
    registry_entry_id: str
) -> ActivationStillDeniedRegistryEntry | None:
    for e in registry:
        if e.registry_entry_id == registry_entry_id:
            return e
    return None

def find_activation_denied_entries_by_candidate_id(
    registry: list[ActivationStillDeniedRegistryEntry],
    candidate_id: str
) -> list[ActivationStillDeniedRegistryEntry]:
    return [e for e in registry if e.candidate_id == candidate_id]

def latest_activation_denied_entry_for_candidate(
    registry: list[ActivationStillDeniedRegistryEntry],
    candidate_id: str
) -> ActivationStillDeniedRegistryEntry | None:
    entries = find_activation_denied_entries_by_candidate_id(registry, candidate_id)
    if not entries:
        return None
    return sorted(entries, key=lambda x: x.created_at_utc, reverse=True)[0]

def activation_denied_registry_summary(registry: list[ActivationStillDeniedRegistryEntry]) -> dict[str, Any]:
    return {
        "total_entries": len(registry),
        "candidates": len(set(e.candidate_id for e in registry if e.candidate_id))
    }

def activation_denied_registry_to_text(registry: list[ActivationStillDeniedRegistryEntry], limit: int = 100) -> str:
    summary = activation_denied_registry_summary(registry)
    return f"Registry Summary: {summary}"
