
from usa_signal_bot.data_providers.provider_abstraction import build_default_provider_abstraction_context
from usa_signal_bot.core.enums import ProviderAbstractionStatus

def test_build_default_provider_abstraction_context():
    ctx = build_default_provider_abstraction_context()
    assert ctx.status == ProviderAbstractionStatus.CREATED
    assert ctx.metadata_only is True
    assert ctx.broker_execution_enabled is False
    assert ctx.scraping_enabled is False
