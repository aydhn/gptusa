import pytest
from usa_signal_bot.advanced_runtime.provider_rate_limit_contracts import build_unknown_rate_limit_metadata

def test_rate_limit():
    m = build_unknown_rate_limit_metadata("test")
    assert m.known is False
