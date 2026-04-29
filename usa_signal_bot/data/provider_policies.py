from dataclasses import dataclass, field
from typing import List, Optional
from usa_signal_bot.core.exceptions import ProviderPolicyError

@dataclass
class RetryPolicy:
    max_attempts: int = 3
    backoff_seconds: float = 1.0
    backoff_multiplier: float = 2.0
    retry_on_errors: List[str] = field(default_factory=lambda: ["Timeout", "ConnectionError", "RateLimit"])

    def __post_init__(self):
        if self.retry_on_errors is None:
            self.retry_on_errors = []

@dataclass
class RateLimitPolicy:
    enabled: bool = True
    min_seconds_between_requests: float = 1.0
    max_requests_per_minute: Optional[int] = 60
    max_symbols_per_batch: int = 50

@dataclass
class CachePolicy:
    enabled: bool = True
    cache_dir: str = "data/cache/provider"
    ttl_seconds: int = 86400
    prefer_cache: bool = True

@dataclass
class DataProviderPolicy:
    retry: RetryPolicy = field(default_factory=RetryPolicy)
    rate_limit: RateLimitPolicy = field(default_factory=RateLimitPolicy)
    cache: CachePolicy = field(default_factory=CachePolicy)

def default_retry_policy() -> RetryPolicy:
    return RetryPolicy()

def default_rate_limit_policy() -> RateLimitPolicy:
    return RateLimitPolicy()

def default_cache_policy() -> CachePolicy:
    return CachePolicy()

def default_data_provider_policy() -> DataProviderPolicy:
    return DataProviderPolicy()

def validate_data_provider_policy(policy: DataProviderPolicy) -> None:
    if policy.retry.max_attempts < 1:
        raise ProviderPolicyError("RetryPolicy 'max_attempts' must be >= 1.")
    if policy.retry.backoff_seconds < 0:
        raise ProviderPolicyError("RetryPolicy 'backoff_seconds' must be >= 0.")
    if policy.retry.backoff_multiplier < 1:
        raise ProviderPolicyError("RetryPolicy 'backoff_multiplier' must be >= 1.")

    if policy.rate_limit.min_seconds_between_requests < 0:
        raise ProviderPolicyError("RateLimitPolicy 'min_seconds_between_requests' must be >= 0.")
    if policy.rate_limit.max_requests_per_minute is not None and policy.rate_limit.max_requests_per_minute <= 0:
         raise ProviderPolicyError("RateLimitPolicy 'max_requests_per_minute' must be None or positive.")
    if policy.rate_limit.max_symbols_per_batch <= 0:
         raise ProviderPolicyError("RateLimitPolicy 'max_symbols_per_batch' must be positive.")

    if policy.cache.ttl_seconds < 0:
        raise ProviderPolicyError("CachePolicy 'ttl_seconds' must be >= 0.")
    if not policy.cache.cache_dir:
         raise ProviderPolicyError("CachePolicy 'cache_dir' must not be empty.")
