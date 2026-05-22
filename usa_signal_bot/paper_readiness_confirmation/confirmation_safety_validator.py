from typing import Any
from usa_signal_bot.paper_readiness_confirmation.confirmation_models import (
    ReadinessConfirmationQueueItem,
    HumanReviewBundle,
    ActivationStillDeniedRegistryEntry
)
from usa_signal_bot.core.enums import ReadinessConfirmationRiskFlag

def collect_confirmation_safety_flags(
    queue_item: ReadinessConfirmationQueueItem | None = None,
    bundle: HumanReviewBundle | None = None,
    registry_entry: ActivationStillDeniedRegistryEntry | None = None
) -> list[ReadinessConfirmationRiskFlag]:
    flags = []

    if queue_item:
        flags.extend(queue_item.safety_flags)
        if queue_item.allows_active_paper:
             flags.append(ReadinessConfirmationRiskFlag.ACTIVE_PAPER_ENABLE_RISK)

    if bundle:
        flags.extend(bundle.safety_flags)
        if bundle.activation_allowed:
             flags.append(ReadinessConfirmationRiskFlag.ACTIVATION_ALLOWED_RISK)

    if registry_entry:
        flags.extend(registry_entry.safety_flags)
        if registry_entry.activation_allowed:
             flags.append(ReadinessConfirmationRiskFlag.ACTIVATION_ALLOWED_RISK)

    return list(set(flags))

def confirmation_has_blocking_flags(flags: list[ReadinessConfirmationRiskFlag]) -> bool:
    blocking = [
        ReadinessConfirmationRiskFlag.REAL_ORDER_RISK,
        ReadinessConfirmationRiskFlag.PAPER_ORDER_RISK,
        ReadinessConfirmationRiskFlag.BROKER_ORDER_RISK,
        ReadinessConfirmationRiskFlag.PAPER_STATE_MUTATION_RISK,
        ReadinessConfirmationRiskFlag.TELEGRAM_REAL_SEND_RISK,
        ReadinessConfirmationRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
        ReadinessConfirmationRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
        ReadinessConfirmationRiskFlag.ACTIVATION_ALLOWED_RISK
    ]
    return any(f in flags for f in blocking)

def validate_confirmation_safety(
    queue_item: ReadinessConfirmationQueueItem | None = None,
    bundle: HumanReviewBundle | None = None,
    registry_entry: ActivationStillDeniedRegistryEntry | None = None
) -> list[str]:
    flags = collect_confirmation_safety_flags(queue_item, bundle, registry_entry)
    errors = []
    if confirmation_has_blocking_flags(flags):
        errors.append("Confirmation contains blocking safety flags.")
    return errors

def confirmation_safety_summary(flags: list[ReadinessConfirmationRiskFlag]) -> dict[str, Any]:
    return {
        "is_safe": not confirmation_has_blocking_flags(flags),
        "blocking_flags": [f.value for f in flags if f in [
            ReadinessConfirmationRiskFlag.REAL_ORDER_RISK,
            ReadinessConfirmationRiskFlag.PAPER_ORDER_RISK,
            ReadinessConfirmationRiskFlag.BROKER_ORDER_RISK,
            ReadinessConfirmationRiskFlag.PAPER_STATE_MUTATION_RISK,
            ReadinessConfirmationRiskFlag.TELEGRAM_REAL_SEND_RISK,
            ReadinessConfirmationRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
            ReadinessConfirmationRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
            ReadinessConfirmationRiskFlag.ACTIVATION_ALLOWED_RISK
        ]]
    }

def confirmation_safety_validator_to_text(payload: dict[str, Any]) -> str:
    return "Safety Validation Executed"
