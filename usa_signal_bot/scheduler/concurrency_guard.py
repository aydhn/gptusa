from typing import List, Optional
from datetime import datetime, timezone
import contextlib

from usa_signal_bot.core.enums import RunLockScope, ConcurrencyDecision, LockAcquisitionMode, RunLockStatus
from usa_signal_bot.scheduler.scheduler_models import (
    RunIdentity, RunLock, LockAcquisitionResult,
    ConcurrencyPolicy, ConcurrencyDecisionResult, create_concurrency_decision_id
)
from usa_signal_bot.scheduler.lock_manager import FileRunLockManager
from usa_signal_bot.scheduler.concurrency_policy import policy_for_scope

class ConcurrencyGuard:
    def __init__(self, lock_manager: FileRunLockManager, policies: Optional[List[ConcurrencyPolicy]] = None):
        self.lock_manager = lock_manager
        self.policies = policies

    def evaluate(self, scope: RunLockScope) -> ConcurrencyDecisionResult:
        now_utc = datetime.now(timezone.utc).isoformat()
        policy = policy_for_scope(scope, self.policies)

        all_locks = self.lock_manager.list_locks(scope=scope)
        # Filter active non-stale locks
        active_locks = [l for l in all_locks if not self.lock_manager.is_lock_stale(l, now_utc)]

        decision = ConcurrencyDecision.ALLOW
        reason = "No active locks conflict"

        if len(active_locks) >= policy.max_concurrent_runs:
            if not policy.allow_overlap:
                decision = ConcurrencyDecision.BLOCK
                reason = f"Max concurrent runs ({policy.max_concurrent_runs}) reached for scope {scope.value}"

        return ConcurrencyDecisionResult(
            decision_id=create_concurrency_decision_id(),
            created_at_utc=now_utc,
            scope=scope,
            decision=decision,
            policy=policy,
            active_locks=active_locks,
            reason=reason
        )

    def active_locks(self, scope: Optional[RunLockScope] = None) -> List[RunLock]:
        now_utc = datetime.now(timezone.utc).isoformat()
        all_locks = self.lock_manager.list_locks(scope=scope)
        return [l for l in all_locks if not self.lock_manager.is_lock_stale(l, now_utc)]

    def can_start(self, scope: RunLockScope) -> bool:
        res = self.evaluate(scope)
        return res.decision == ConcurrencyDecision.ALLOW

    def acquire_or_block(self, scope: RunLockScope, owner: RunIdentity, mode: Optional[LockAcquisitionMode] = None) -> LockAcquisitionResult:
        policy = policy_for_scope(scope, self.policies)
        res = self.evaluate(scope)

        if res.decision == ConcurrencyDecision.BLOCK and mode != LockAcquisitionMode.DRY_RUN:
            return LockAcquisitionResult(
                result_id=create_concurrency_decision_id("acq_blocked"),
                created_at_utc=datetime.now(timezone.utc).isoformat(),
                status=RunLockStatus.BLOCKED,
                scope=scope,
                acquired=False,
                lock=None,
                existing_lock=res.active_locks[0] if res.active_locks else None,
                mode=mode or policy.acquisition_mode,
                errors=[res.reason]
            )

        return self.lock_manager.acquire(scope, owner, policy, mode)

    def release_if_owned(self, lock: RunLock, owner: RunIdentity) -> RunLock:
        return self.lock_manager.release(lock, owner)

    @contextlib.contextmanager
    def guard_context(self, scope: RunLockScope, owner: RunIdentity, mode: Optional[LockAcquisitionMode] = None):
        acq_result = self.acquire_or_block(scope, owner, mode)
        if not acq_result.acquired and acq_result.mode != LockAcquisitionMode.DRY_RUN:
            raise RuntimeError(f"Concurrency Blocked for scope {scope.value}: {acq_result.errors}")

        try:
            yield acq_result
        finally:
            if acq_result.lock:
                try:
                    self.release_if_owned(acq_result.lock, owner)
                except Exception:
                    pass
