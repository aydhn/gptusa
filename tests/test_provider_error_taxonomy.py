import pytest
from usa_signal_bot.advanced_runtime.provider_error_taxonomy import provider_error_is_blocking

def test_taxonomy():
    assert provider_error_is_blocking("PAID_API_BLOCKED") is True
