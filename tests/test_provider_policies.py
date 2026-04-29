import pytest
from usa_signal_bot.data.provider_policies import (
    RetryPolicy, RateLimitPolicy, CachePolicy, DataProviderPolicy,
    default_retry_policy, default_rate_limit_policy,
    default_cache_policy, default_data_provider_policy,
    validate_data_provider_policy
)
from usa_signal_bot.core.exceptions import ProviderPolicyError

def test_default_policies_are_valid():
    policy = default_data_provider_policy()
    validate_data_provider_policy(policy)

def test_retry_policy_invalid_max_attempts():
    policy = DataProviderPolicy(retry=RetryPolicy(max_attempts=0))
    with pytest.raises(ProviderPolicyError):
        validate_data_provider_policy(policy)

def test_retry_policy_invalid_backoff_multiplier():
    policy = DataProviderPolicy(retry=RetryPolicy(backoff_multiplier=0.5))
    with pytest.raises(ProviderPolicyError):
        validate_data_provider_policy(policy)

def test_rate_limit_policy_invalid_batch():
    policy = DataProviderPolicy(rate_limit=RateLimitPolicy(max_symbols_per_batch=0))
    with pytest.raises(ProviderPolicyError):
        validate_data_provider_policy(policy)

def test_cache_policy_invalid_ttl():
    policy = DataProviderPolicy(cache=CachePolicy(ttl_seconds=-10))
    with pytest.raises(ProviderPolicyError):
        validate_data_provider_policy(policy)
