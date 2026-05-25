
from usa_signal_bot.data_providers.provider_registry_validator import validate_provider_registry

def test_registry_validator():
    errs = validate_provider_registry([])
    assert len(errs) == 0
