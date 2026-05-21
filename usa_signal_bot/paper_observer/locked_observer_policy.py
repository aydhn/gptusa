from datetime import datetime, timezone
from typing import List
from usa_signal_bot.core.enums import ObserverOutputType, ObserverSafetyFlag
from usa_signal_bot.paper_observer.observer_models import LockedObserverPolicy, create_locked_observer_policy_id

def allowed_observer_output_types() -> List[ObserverOutputType]:
    return [
        ObserverOutputType.SIGNAL_MIRROR,
        ObserverOutputType.PROPOSAL_MIRROR,
        ObserverOutputType.RISK_MIRROR,
        ObserverOutputType.NOTIFICATION_PREVIEW,
        ObserverOutputType.PAPER_SNAPSHOT_SUMMARY,
        ObserverOutputType.DRIFT_EVENT,
        ObserverOutputType.SAFETY_EVENT
    ]

def default_locked_observer_policy() -> LockedObserverPolicy:
    return LockedObserverPolicy(
        policy_id=create_locked_observer_policy_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        require_human_approval=True,
        require_planning_ticket=True,
        locked_runtime=True,
        allow_active_paper=False,
        allow_paper_state_mutation=False,
        allow_paper_orders=False,
        allow_broker_orders=False,
        allow_telegram_real_send=False,
        allow_config_patch=False,
        allowed_output_types=allowed_observer_output_types(),
        warnings=[],
        errors=[],
        metadata={}
    )

def strict_locked_observer_policy() -> LockedObserverPolicy:
    return default_locked_observer_policy()

def validate_locked_policy_safety(policy: LockedObserverPolicy) -> List[str]:
    errors = []
    if not policy.locked_runtime:
        errors.append("Policy must have locked_runtime=True")
    if policy.allow_active_paper:
        errors.append("Policy cannot allow active paper")
    if policy.allow_paper_state_mutation:
        errors.append("Policy cannot allow paper state mutation")
    if policy.allow_paper_orders:
        errors.append("Policy cannot allow paper orders")
    if policy.allow_broker_orders:
        errors.append("Policy cannot allow broker orders")
    if policy.allow_telegram_real_send:
        errors.append("Policy cannot allow Telegram real send")
    if policy.allow_config_patch:
        errors.append("Policy cannot allow config patch")
    return errors

def locked_observer_policy_to_text(policy: LockedObserverPolicy) -> str:
    return f"LockedObserverPolicy {policy.policy_id} (Locked: {policy.locked_runtime})"
