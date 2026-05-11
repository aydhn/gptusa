import pytest
from usa_signal_bot.core.enums import ResourceProfileScope
from usa_signal_bot.core.exceptions import ThrottlingPolicyError
from usa_signal_bot.profiling.throttling_policy import default_throttling_policies, policy_for_profile_scope, validate_throttling_policy

def test_default_policies():
    policies = default_throttling_policies()
    assert len(policies) > 0
    assert any(p.scope == ResourceProfileScope.SCAN for p in policies)

def test_policy_for_profile_scope():
    policies = default_throttling_policies()
    scan_policy = policy_for_profile_scope(ResourceProfileScope.SCAN, policies)
    assert scan_policy.scope == ResourceProfileScope.SCAN

    unknown_policy = policy_for_profile_scope(ResourceProfileScope.CUSTOM, policies)
    assert unknown_policy.scope == ResourceProfileScope.CUSTOM

def test_validate_throttling_policy():
    policies = default_throttling_policies()
    validate_throttling_policy(policies[0])

    bad_policy = policies[0]
    bad_policy.max_wall_time_seconds = -1.0

    with pytest.raises(ThrottlingPolicyError):
        validate_throttling_policy(bad_policy)
