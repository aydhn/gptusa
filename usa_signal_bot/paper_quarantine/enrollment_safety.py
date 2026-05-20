from typing import Any

from usa_signal_bot.core.enums import QuarantineSafetyFlag
from usa_signal_bot.paper_quarantine.quarantine_models import (
    QuarantinedPaperCandidate,
    ReadOnlyPromotionTicket,
    SupervisedDryRunBridgePlan,
)
from usa_signal_bot.paper_quarantine.review_window import quarantine_review_expired

def collect_quarantine_safety_flags(
    candidate: QuarantinedPaperCandidate,
    ticket: ReadOnlyPromotionTicket | None = None,
    bridge_plan: SupervisedDryRunBridgePlan | None = None
) -> list[QuarantineSafetyFlag]:

    flags = candidate.risk_flags.copy()

    if candidate.allowed_for_active_paper:
        flags.append(QuarantineSafetyFlag.AUTO_ENABLE_RISK)
    if candidate.allowed_for_broker_execution:
        flags.append(QuarantineSafetyFlag.REAL_ORDER_RISK)

    if ticket:
        if ticket.allowed_for_active_paper:
            flags.append(QuarantineSafetyFlag.AUTO_ENABLE_RISK)
        if ticket.allowed_for_config_patch:
            flags.append(QuarantineSafetyFlag.PRODUCTION_CONFIG_WRITE_RISK)
        if ticket.allowed_for_broker_execution:
            flags.append(QuarantineSafetyFlag.REAL_ORDER_RISK)

    if bridge_plan:
        if bridge_plan.paper_state_mutation_enabled:
            flags.append(QuarantineSafetyFlag.PAPER_STATE_MUTATION_RISK)
        if bridge_plan.paper_order_enabled:
            flags.append(QuarantineSafetyFlag.PAPER_ORDER_RISK)
        if bridge_plan.broker_order_enabled:
            flags.append(QuarantineSafetyFlag.REAL_ORDER_RISK)
        if bridge_plan.telegram_real_send_enabled:
             flags.append(QuarantineSafetyFlag.TELEGRAM_REAL_SEND_RISK)
        if bridge_plan.production_config_write_enabled:
             flags.append(QuarantineSafetyFlag.PRODUCTION_CONFIG_WRITE_RISK)

    if quarantine_review_expired(candidate.review_due_at_utc):
        flags.append(QuarantineSafetyFlag.EXPIRED_REVIEW_WINDOW)

    return list(set(flags))

def quarantine_has_blocking_flags(flags: list[QuarantineSafetyFlag]) -> bool:
    blocking = [
        QuarantineSafetyFlag.REAL_ORDER_RISK,
        QuarantineSafetyFlag.PAPER_STATE_MUTATION_RISK,
        QuarantineSafetyFlag.PAPER_ORDER_RISK,
        QuarantineSafetyFlag.TELEGRAM_REAL_SEND_RISK,
        QuarantineSafetyFlag.PRODUCTION_CONFIG_WRITE_RISK,
        QuarantineSafetyFlag.AUTO_ENABLE_RISK,
        QuarantineSafetyFlag.BLOCKED_SHADOW_DECISION,
        QuarantineSafetyFlag.EXPIRED_REVIEW_WINDOW,
    ]
    for flag in blocking:
        if flag in flags:
            return True
    return False

def validate_quarantine_enrollment_safety(
    candidate: QuarantinedPaperCandidate,
    ticket: ReadOnlyPromotionTicket | None = None,
    bridge_plan: SupervisedDryRunBridgePlan | None = None
) -> list[str]:
    flags = collect_quarantine_safety_flags(candidate, ticket, bridge_plan)
    errors = []

    if QuarantineSafetyFlag.REAL_ORDER_RISK in flags:
        errors.append("Real order risk detected.")
    if QuarantineSafetyFlag.PAPER_STATE_MUTATION_RISK in flags:
        errors.append("Paper state mutation risk detected.")
    if QuarantineSafetyFlag.PAPER_ORDER_RISK in flags:
        errors.append("Paper order risk detected.")
    if QuarantineSafetyFlag.TELEGRAM_REAL_SEND_RISK in flags:
        errors.append("Telegram real send risk detected.")
    if QuarantineSafetyFlag.PRODUCTION_CONFIG_WRITE_RISK in flags:
        errors.append("Production config write risk detected.")
    if QuarantineSafetyFlag.AUTO_ENABLE_RISK in flags:
        errors.append("Auto enable risk detected.")
    if QuarantineSafetyFlag.BLOCKED_SHADOW_DECISION in flags:
        errors.append("Blocked shadow decision.")
    if QuarantineSafetyFlag.EXPIRED_REVIEW_WINDOW in flags:
        errors.append("Expired review window.")

    return errors

def build_quarantine_safety_summary(flags: list[QuarantineSafetyFlag]) -> dict[str, Any]:
    return {
        "flags": [f.value for f in flags],
        "has_blocking": quarantine_has_blocking_flags(flags),
    }

def enrollment_safety_to_text(payload: dict[str, Any]) -> str:
    flags = payload.get("flags", [])
    has_blocking = payload.get("has_blocking", False)

    lines = [
        "Enrollment Safety Summary",
        f"Flags: {flags}",
        f"Has Blocking: {has_blocking}"
    ]
    return "\n".join(lines)
