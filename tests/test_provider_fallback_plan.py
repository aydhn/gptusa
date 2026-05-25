
from usa_signal_bot.data_providers.provider_fallback_plan import build_provider_fallback_plan
from usa_signal_bot.core.enums import DataProviderKind, DataProviderCapability

def test_provider_fallback_plan():
    plan = build_provider_fallback_plan(DataProviderKind.MARKET_DATA, DataProviderCapability.GET_DAILY_OHLCV)
    assert plan.network_allowed is False
    assert plan.broker_allowed is False
    assert plan.plan_safe is True
