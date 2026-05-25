
from usa_signal_bot.data_providers.provider_safety_policy import build_provider_safety_policy

def test_provider_safety_policy():
    policy = build_provider_safety_policy()
    assert policy.network_fetch_disabled_now is True
    assert policy.scraping_blocked is True
    assert policy.broker_blocked is True
