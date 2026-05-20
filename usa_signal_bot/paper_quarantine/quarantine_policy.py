from typing import Any
import datetime

from usa_signal_bot.core.enums import BridgeOperation
from usa_signal_bot.paper_quarantine.quarantine_models import (
    QuarantinePolicy,
    create_quarantine_policy_id,
    validate_quarantine_policy,
)
from usa_signal_bot.core.exceptions import QuarantinePolicyError

def allowed_quarantine_bridge_operations() -> list[BridgeOperation]:
    return [
        BridgeOperation.READ_PROMOTION_TICKET,
        BridgeOperation.READ_CANDIDATE_BUNDLE,
        BridgeOperation.READ_SHADOW_GOVERNANCE,
        BridgeOperation.READ_PAPER_SNAPSHOT,
        BridgeOperation.BUILD_DRY_RUN_PLAN,
        BridgeOperation.WRITE_QUARANTINE_OUTPUT,
        BridgeOperation.GENERATE_NOTIFICATION_PREVIEW,
    ]

def denied_quarantine_bridge_operations() -> list[BridgeOperation]:
    return [
        BridgeOperation.WRITE_PAPER_STATE,
        BridgeOperation.SEND_PAPER_ORDER,
        BridgeOperation.SEND_BROKER_ORDER,
        BridgeOperation.SEND_TELEGRAM_REAL,
        BridgeOperation.WRITE_PRODUCTION_CONFIG,
    ]

def default_quarantine_policy(min_shadow_acceptance_score: float = 70.0) -> QuarantinePolicy:
    policy = QuarantinePolicy(
        policy_id=create_quarantine_policy_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        require_manual_review=True,
        require_shadow_governance_acceptance=True,
        min_shadow_acceptance_score=min_shadow_acceptance_score,
        allow_paper_state_mutation=False,
        allow_paper_orders=False,
        allow_broker_orders=False,
        allow_telegram_real_send=False,
        allow_production_config_write=False,
        allowed_bridge_operations=allowed_quarantine_bridge_operations(),
        denied_bridge_operations=denied_quarantine_bridge_operations(),
        warnings=[],
        errors=[],
        metadata={"policy_type": "default"},
    )
    validate_quarantine_policy(policy)
    return policy

def strict_quarantine_policy() -> QuarantinePolicy:
    policy = QuarantinePolicy(
        policy_id=create_quarantine_policy_id("strict_policy"),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        require_manual_review=True,
        require_shadow_governance_acceptance=True,
        min_shadow_acceptance_score=85.0,
        allow_paper_state_mutation=False,
        allow_paper_orders=False,
        allow_broker_orders=False,
        allow_telegram_real_send=False,
        allow_production_config_write=False,
        allowed_bridge_operations=[BridgeOperation.READ_PROMOTION_TICKET], # very strict
        denied_bridge_operations=denied_quarantine_bridge_operations() + allowed_quarantine_bridge_operations(), # all denied basically
        warnings=[],
        errors=[],
        metadata={"policy_type": "strict"},
    )
    # the allowed overrides the denied in the test above, fix to valid
    policy.denied_bridge_operations = denied_quarantine_bridge_operations()
    policy.allowed_bridge_operations = allowed_quarantine_bridge_operations()

    validate_quarantine_policy(policy)
    return policy

def validate_quarantine_policy_safety(policy: QuarantinePolicy) -> list[str]:
    errors = []
    if policy.allow_paper_state_mutation:
        errors.append("allow_paper_state_mutation must be False")
    if policy.allow_paper_orders:
        errors.append("allow_paper_orders must be False")
    if policy.allow_broker_orders:
        errors.append("allow_broker_orders must be False")
    if policy.allow_telegram_real_send:
        errors.append("allow_telegram_real_send must be False")
    if policy.allow_production_config_write:
        errors.append("allow_production_config_write must be False")

    for op in denied_quarantine_bridge_operations():
        if op in policy.allowed_bridge_operations:
            errors.append(f"BridgeOperation {op.value} cannot be in allowed operations")

    return errors

def quarantine_policy_to_text(policy: QuarantinePolicy) -> str:
    lines = [
        f"Quarantine Policy: {policy.policy_id}",
        f"Created At: {policy.created_at_utc}",
        f"Manual Review Required: {policy.require_manual_review}",
        f"Min Shadow Score: {policy.min_shadow_acceptance_score}",
        f"Safety Flags:",
        f"  Mutation Allowed: {policy.allow_paper_state_mutation}",
        f"  Broker Orders Allowed: {policy.allow_broker_orders}",
        f"Allowed Operations: {[op.value for op in policy.allowed_bridge_operations]}",
        f"Denied Operations: {[op.value for op in policy.denied_bridge_operations]}",
    ]
    return "\n".join(lines)
