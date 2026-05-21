from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import ObserverSafetyFlag
from usa_signal_bot.paper_observer.observer_models import (
    LockedObserverPolicy,
    PaperObserverEnrollment,
    ObserverRuntimeContext,
    ObserverOutput,
    ObserverRuntimeSession
)

def collect_observer_safety_flags_from_policy(policy: LockedObserverPolicy) -> List[ObserverSafetyFlag]:
    flags = []
    if not policy.locked_runtime:
        flags.append(ObserverSafetyFlag.OBSERVER_UNLOCK_RISK)
    if policy.allow_active_paper:
        flags.append(ObserverSafetyFlag.ACTIVE_PAPER_ENABLE_RISK)
    return flags

def collect_observer_safety_flags_from_enrollment(enrollment: PaperObserverEnrollment) -> List[ObserverSafetyFlag]:
    return list(enrollment.safety_flags)

def collect_observer_safety_flags_from_context(context: ObserverRuntimeContext) -> List[ObserverSafetyFlag]:
    flags = []
    if not context.locked:
        flags.append(ObserverSafetyFlag.OBSERVER_UNLOCK_RISK)
    if context.allow_broker_orders:
        flags.append(ObserverSafetyFlag.BROKER_ORDER_RISK)
    if context.allow_paper_state_mutation:
        flags.append(ObserverSafetyFlag.PAPER_STATE_MUTATION_RISK)
    return flags

def collect_observer_safety_flags_from_outputs(outputs: List[ObserverOutput]) -> List[ObserverSafetyFlag]:
    flags = set()
    for o in outputs:
        for f in o.safety_flags:
            flags.add(f)
    return list(flags)

def observer_has_blocking_flags(flags: List[ObserverSafetyFlag]) -> bool:
    blocking_flags = [
        ObserverSafetyFlag.REAL_ORDER_RISK,
        ObserverSafetyFlag.PAPER_ORDER_RISK,
        ObserverSafetyFlag.BROKER_ORDER_RISK,
        ObserverSafetyFlag.PAPER_STATE_MUTATION_RISK,
        ObserverSafetyFlag.TELEGRAM_REAL_SEND_RISK,
        ObserverSafetyFlag.PRODUCTION_CONFIG_WRITE_RISK,
        ObserverSafetyFlag.ACTIVE_PAPER_ENABLE_RISK,
        ObserverSafetyFlag.OBSERVER_UNLOCK_RISK
    ]
    return any(f in blocking_flags for f in flags)

def validate_observer_runtime_safety(
    enrollment: Optional[PaperObserverEnrollment] = None,
    context: Optional[ObserverRuntimeContext] = None,
    session: Optional[ObserverRuntimeSession] = None
) -> List[str]:
    errors = []
    flags = set()
    if enrollment:
        for f in collect_observer_safety_flags_from_enrollment(enrollment): flags.add(f)
        if enrollment.policy:
            for f in collect_observer_safety_flags_from_policy(enrollment.policy): flags.add(f)

    if context:
        for f in collect_observer_safety_flags_from_context(context): flags.add(f)

    if session:
        for f in collect_observer_safety_flags_from_outputs(session.outputs): flags.add(f)

    if observer_has_blocking_flags(list(flags)):
        errors.append(f"Observer has blocking safety flags: {[f.value for f in flags]}")

    return errors

def observer_runtime_safety_to_text(payload: Dict[str, Any]) -> str:
    return f"Safety validation performed. Payload size: {len(payload)}"
