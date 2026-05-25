from usa_signal_bot.data_provider_runtime.provider_runtime_registry import build_provider_runtime_adapter_specs, validate_provider_runtime_registry

def test_provider_runtime_registry():
    specs = build_provider_runtime_adapter_specs()
    assert len(specs) == 3
    errors = validate_provider_runtime_registry(specs)
    assert len(errors) == 0
