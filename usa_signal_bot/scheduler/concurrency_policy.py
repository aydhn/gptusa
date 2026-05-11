from typing import List, Dict, Any, Optional
from usa_signal_bot.core.enums import RunLockScope, LockAcquisitionMode
from usa_signal_bot.scheduler.scheduler_models import ConcurrencyPolicy, create_concurrency_policy_id

def default_concurrency_policies() -> List[ConcurrencyPolicy]:
    return [
        ConcurrencyPolicy(
            policy_id=create_concurrency_policy_id(RunLockScope.GLOBAL),
            scope=RunLockScope.GLOBAL,
            enabled=True,
            max_concurrent_runs=1,
            allow_overlap=False,
            stale_after_seconds=7200,
            wait_timeout_seconds=0,
            acquisition_mode=LockAcquisitionMode.FAIL_FAST,
            description="Default Global Lock"
        ),
        ConcurrencyPolicy(
            policy_id=create_concurrency_policy_id(RunLockScope.SCAN),
            scope=RunLockScope.SCAN,
            enabled=True,
            max_concurrent_runs=1,
            allow_overlap=False,
            stale_after_seconds=3600,
            wait_timeout_seconds=0,
            acquisition_mode=LockAcquisitionMode.FAIL_FAST
        ),
        ConcurrencyPolicy(
            policy_id=create_concurrency_policy_id(RunLockScope.BACKTEST),
            scope=RunLockScope.BACKTEST,
            enabled=True,
            max_concurrent_runs=1,
            allow_overlap=False,
            stale_after_seconds=7200,
            wait_timeout_seconds=0,
            acquisition_mode=LockAcquisitionMode.FAIL_FAST
        ),
        ConcurrencyPolicy(
            policy_id=create_concurrency_policy_id(RunLockScope.PAPER),
            scope=RunLockScope.PAPER,
            enabled=True,
            max_concurrent_runs=1,
            allow_overlap=False,
            stale_after_seconds=3600,
            wait_timeout_seconds=0,
            acquisition_mode=LockAcquisitionMode.FAIL_FAST
        ),
        ConcurrencyPolicy(
            policy_id=create_concurrency_policy_id(RunLockScope.REGRESSION),
            scope=RunLockScope.REGRESSION,
            enabled=True,
            max_concurrent_runs=1,
            allow_overlap=False,
            stale_after_seconds=7200,
            wait_timeout_seconds=0,
            acquisition_mode=LockAcquisitionMode.FAIL_FAST
        ),
        ConcurrencyPolicy(
            policy_id=create_concurrency_policy_id(RunLockScope.RETENTION),
            scope=RunLockScope.RETENTION,
            enabled=True,
            max_concurrent_runs=1,
            allow_overlap=False,
            stale_after_seconds=3600,
            wait_timeout_seconds=0,
            acquisition_mode=LockAcquisitionMode.FAIL_FAST
        ),
        ConcurrencyPolicy(
            policy_id=create_concurrency_policy_id(RunLockScope.OBSERVABILITY),
            scope=RunLockScope.OBSERVABILITY,
            enabled=True,
            max_concurrent_runs=2,
            allow_overlap=True,
            stale_after_seconds=3600,
            wait_timeout_seconds=0,
            acquisition_mode=LockAcquisitionMode.WAIT
        ),
        ConcurrencyPolicy(
            policy_id=create_concurrency_policy_id(RunLockScope.NOTIFICATION),
            scope=RunLockScope.NOTIFICATION,
            enabled=True,
            max_concurrent_runs=1,
            allow_overlap=False,
            stale_after_seconds=1200,
            wait_timeout_seconds=0,
            acquisition_mode=LockAcquisitionMode.FAIL_FAST
        )
    ]

def policy_for_scope(scope: RunLockScope, policies: Optional[List[ConcurrencyPolicy]] = None) -> ConcurrencyPolicy:
    policies = policies or default_concurrency_policies()
    for p in policies:
        if p.scope == scope:
            return p
    # Fallback default
    return ConcurrencyPolicy(
        policy_id=create_concurrency_policy_id(scope),
        scope=scope,
        enabled=True,
        max_concurrent_runs=1,
        allow_overlap=False,
        stale_after_seconds=3600,
        wait_timeout_seconds=0,
        acquisition_mode=LockAcquisitionMode.FAIL_FAST,
        description=f"Auto-generated for {scope.value}"
    )

def load_concurrency_policies_from_config(config_dict: Optional[Dict[str, Any]] = None) -> List[ConcurrencyPolicy]:
    # Placeholder for converting ConfigSchema to ConcurrencyPolicy list if needed
    return default_concurrency_policies()

def concurrency_policies_to_text(policies: List[ConcurrencyPolicy]) -> str:
    lines = ["Concurrency Policies:"]
    for p in policies:
        lines.append(f" - {p.scope.value}: Max {p.max_concurrent_runs}, AllowOverlap: {p.allow_overlap}, Mode: {p.acquisition_mode.value}")
    return "\n".join(lines)
