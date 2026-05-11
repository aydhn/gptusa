from usa_signal_bot.scheduler.concurrency_policy import (
    default_concurrency_policies, policy_for_scope, concurrency_policies_to_text
)
from usa_signal_bot.core.enums import RunLockScope

def test_default_policies_non_empty():
    policies = default_concurrency_policies()
    assert len(policies) > 0

def test_policy_for_scope():
    p = policy_for_scope(RunLockScope.SCAN)
    assert p.scope == RunLockScope.SCAN
    assert p.max_concurrent_runs > 0

def test_concurrency_policies_to_text():
    policies = default_concurrency_policies()
    txt = concurrency_policies_to_text(policies)
    assert "Concurrency Policies:" in txt
    assert "SCAN:" in txt
