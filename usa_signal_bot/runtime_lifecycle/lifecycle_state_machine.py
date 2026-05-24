from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import RuntimeLifecycleStatus, LifecycleTransitionStatus, LifecycleRiskFlag
from usa_signal_bot.runtime_lifecycle.phase104_models import LifecycleTransition, create_lifecycle_transition_id, _now_str
from usa_signal_bot.runtime_lifecycle.lifecycle_policy import build_phase104_lifecycle_policy, lifecycle_policy_allows_transition, validate_lifecycle_policy
from usa_signal_bot.core.exceptions import LifecycleStateMachineError

class RuntimeLifecycleStateMachine:
    def __init__(self, initial_status: RuntimeLifecycleStatus = RuntimeLifecycleStatus.DRAFT, policy: Optional[Dict[str, Any]] = None):
        self._status = initial_status
        self._policy = policy or build_phase104_lifecycle_policy()
        self._history: List[LifecycleTransition] = []

        policy_errors = validate_lifecycle_policy(self._policy)
        if policy_errors:
            raise LifecycleStateMachineError(f"Invalid lifecycle policy: {', '.join(policy_errors)}")

    def current_status(self) -> RuntimeLifecycleStatus:
        return self._status

    def can_transition(self, to_status: RuntimeLifecycleStatus) -> bool:
        return lifecycle_policy_allows_transition(self._status, to_status, self._policy)

    def transition(self, to_status: RuntimeLifecycleStatus, reason: str) -> LifecycleTransition:
        if not self.can_transition(to_status):
            t = LifecycleTransition(
                transition_id=create_lifecycle_transition_id(),
                created_at_utc=_now_str(),
                from_status=self._status,
                to_status=to_status,
                transition_status=LifecycleTransitionStatus.BLOCKED,
                allowed=False,
                metadata_only=True,
                read_only=True,
                reason=f"Transition from {self._status.value} to {to_status.value} blocked by policy. {reason}",
                risk_flags=[LifecycleRiskFlag.EXECUTION_ROUTE_RISK],
                warnings=["Unsafe transition blocked"],
                errors=["Policy violation"],
                metadata={}
            )
            self._history.append(t)
            self._status = RuntimeLifecycleStatus.BLOCKED
            return t

        t = LifecycleTransition(
            transition_id=create_lifecycle_transition_id(),
            created_at_utc=_now_str(),
            from_status=self._status,
            to_status=to_status,
            transition_status=LifecycleTransitionStatus.ALLOWED_METADATA_ONLY,
            allowed=True,
            metadata_only=True,
            read_only=True,
            reason=reason,
            risk_flags=[],
            warnings=[],
            errors=[],
            metadata={}
        )
        self._history.append(t)
        self._status = to_status
        return t

    def history(self) -> List[LifecycleTransition]:
        return list(self._history)

    def validate_state_machine_safety(self) -> List[str]:
        return validate_lifecycle_policy(self._policy)
