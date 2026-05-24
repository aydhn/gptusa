import pytest
from usa_signal_bot.advanced_runtime.provider_interface_validator import validate_provider_interface_contract

def test_validator():
    assert len(validate_provider_interface_contract(None)) == 0
