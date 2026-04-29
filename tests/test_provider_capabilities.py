import pytest
from usa_signal_bot.data.provider_capabilities import (
    ProviderCapability, validate_provider_capability,
    default_mock_provider_capability, reserved_yfinance_provider_capability
)
from usa_signal_bot.core.exceptions import ProviderCapabilityError

def test_default_mock_capability_is_valid():
    cap = default_mock_provider_capability()
    validate_provider_capability(cap)

def test_reserved_yfinance_capability_is_valid():
    cap = reserved_yfinance_provider_capability()
    validate_provider_capability(cap)

def test_capability_requires_name():
    cap = ProviderCapability(provider_name="")
    with pytest.raises(ProviderCapabilityError):
        validate_provider_capability(cap)

def test_capability_must_be_free_only():
    cap = ProviderCapability(provider_name="test", free_only=False)
    with pytest.raises(ProviderCapabilityError):
        validate_provider_capability(cap)

def test_capability_cannot_allow_scraping():
    cap = ProviderCapability(provider_name="test", allows_scraping=True)
    with pytest.raises(ProviderCapabilityError):
        validate_provider_capability(cap)

def test_capability_cannot_require_api_key():
    cap = ProviderCapability(provider_name="test", requires_api_key=True)
    with pytest.raises(ProviderCapabilityError):
        validate_provider_capability(cap)
