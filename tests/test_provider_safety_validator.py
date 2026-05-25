
from usa_signal_bot.data_providers.provider_safety_validator import validate_provider_abstraction_safety
from usa_signal_bot.data_providers.provider_abstraction import build_default_provider_abstraction_context

def test_safety_validator():
    ctx = build_default_provider_abstraction_context()
    errs = validate_provider_abstraction_safety(ctx)
    assert len(errs) == 0
