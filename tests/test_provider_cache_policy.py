import pytest
from usa_signal_bot.advanced_runtime.provider_cache_policy import build_default_provider_cache_policy

def test_cache():
    p = build_default_provider_cache_policy("test")
    assert p.cache_enabled is True
