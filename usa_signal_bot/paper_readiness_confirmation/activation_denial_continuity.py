from typing import Any
from usa_signal_bot.paper_readiness_confirmation.confirmation_models import (
    ReadinessConfirmationQueueItem,
    HumanReviewBundle,
    ActivationStillDeniedRegistryEntry
)
from usa_signal_bot.core.enums import ReadinessConfirmationRiskFlag

def validate_activation_denial_continuity(
    queue_item: ReadinessConfirmationQueueItem | None = None,
    bundle: HumanReviewBundle | None = None,
    registry_entry: ActivationStillDeniedRegistryEntry | None = None
) -> list[str]:
    errors = []

    if queue_item:
         if not queue_item.activation_denied_required:
             errors.append("Queue item missing activation_denied_required")
         if queue_item.allows_active_paper:
             errors.append("Queue item allows active paper")

    if bundle:
         if not bundle.activation_denied:
             errors.append("Bundle missing activation_denied")
         if bundle.activation_allowed:
             errors.append("Bundle allows activation")

    if registry_entry:
         if not registry_entry.activation_denied:
             errors.append("Registry entry missing activation_denied")
         if registry_entry.activation_allowed:
             errors.append("Registry entry allows activation")

    return errors

def activation_denial_continuity_flags(payload: dict[str, Any]) -> list[ReadinessConfirmationRiskFlag]:
    flags = []
    if payload.get("activation_allowed"):
         flags.append(ReadinessConfirmationRiskFlag.ACTIVATION_ALLOWED_RISK)
    if not payload.get("activation_denied", True):
         flags.append(ReadinessConfirmationRiskFlag.ACTIVATION_DENIAL_MISSING)
    return flags

def activation_denial_continuity_summary(payload: dict[str, Any]) -> dict[str, Any]:
    flags = activation_denial_continuity_flags(payload)
    return {
        "is_continuous": len(flags) == 0,
        "flags": [f.value for f in flags]
    }

def activation_denial_is_preserved(payload: dict[str, Any]) -> bool:
    return len(activation_denial_continuity_flags(payload)) == 0

def activation_denial_continuity_to_text(payload: dict[str, Any]) -> str:
    summary = activation_denial_continuity_summary(payload)
    return f"Denial Continuous: {summary['is_continuous']}"
