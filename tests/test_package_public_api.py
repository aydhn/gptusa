import importlib

import pytest

PACKAGES = {
    "usa_signal_bot.core": ["DataProviderName", "RunLockScope", "SignalAction", "USASignalBotError"],
    "usa_signal_bot.data": ["MarketDataRequest", "MarketDataResponse", "OHLCVBar"],
    "usa_signal_bot.features": ["Indicator", "IndicatorMetadata", "IndicatorParameterSchema", "IndicatorParameterSpec"],
}


@pytest.mark.parametrize("package", sorted(PACKAGES))
def test_public_api_is_importable_and_listed(package):
    module = importlib.import_module(package)
    for name in PACKAGES[package]:
        assert hasattr(module, name), name
        assert name in module.__all__
