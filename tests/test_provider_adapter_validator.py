
from usa_signal_bot.data_providers.provider_adapter_validator import validate_provider_adapter_spec
from usa_signal_bot.data_providers.phase106_models import ProviderAdapterSpec
from usa_signal_bot.core.enums import DataProviderName, DataProviderKind, DataProviderAdapterStatus, DataProviderAdapterDecision

def test_adapter_validator():
    spec = ProviderAdapterSpec(
        adapter_id="a1", created_at_utc="2023", provider_name=DataProviderName.YFINANCE,
        provider_kind=DataProviderKind.MARKET_DATA, adapter_status=DataProviderAdapterStatus.SKELETON,
        adapter_decision=DataProviderAdapterDecision.REGISTER_SKELETON, permissions=[], capabilities=[],
        domains=[], supports_cache=False, supports_local_fixture=False, supports_rate_limit_metadata=False,
        supports_quality_hints=False, requires_api_key=False, paid_api=False, scraping_required=False,
        html_parsing_required=False, broker_related=False, order_related=False, network_fetch_enabled_now=False,
        network_fetch_future_allowed=True, credential_required_now=False, skeleton_only=True
    )
    errs = validate_provider_adapter_spec(spec)
    assert len(errs) == 0

    bad_spec = spec
    bad_spec.scraping_required = True
    errs_bad = validate_provider_adapter_spec(bad_spec)
    assert len(errs_bad) > 0
