from usa_signal_bot.feature_engine.core_indicators.indicator_implementation_registry import (
    build_core_indicator_computation_specs, indicator_spec_by_name, validate_indicator_implementation_registry
)

def test_registry():
    specs = build_core_indicator_computation_specs()
    assert len(specs) >= 20

    spec = indicator_spec_by_name("sma_20", specs)
    assert spec is not None
