from usa_signal_bot.core.enums import DataProviderName, DataProviderType, ProviderCapability, ProviderRequestType
from usa_signal_bot.providers.provider_models import ProviderCapabilityProfile, ProviderRequest

def yfinance_capability_profile() -> ProviderCapabilityProfile:
    return ProviderCapabilityProfile(
        provider_name=DataProviderName.YFINANCE,
        provider_type=DataProviderType.ONLINE_FREE_LIBRARY,
        capabilities=[
            ProviderCapability.OHLCV_DAILY,
            ProviderCapability.OHLCV_INTRADAY,
            ProviderCapability.ADJUSTED_CLOSE,
            ProviderCapability.DIVIDENDS,
            ProviderCapability.SPLITS,
            ProviderCapability.SYMBOL_METADATA,
            ProviderCapability.BULK_DOWNLOAD,
            ProviderCapability.SINGLE_SYMBOL
        ],
        requires_api_key=False,
        supports_offline=False,
        supports_bulk=True,
        supports_adjusted=True,
        notes=["yfinance is not an official feed and subject to rate limits"]
    )

def local_cache_capability_profile() -> ProviderCapabilityProfile:
    return ProviderCapabilityProfile(
        provider_name=DataProviderName.LOCAL_CACHE,
        provider_type=DataProviderType.LOCAL_CACHE,
        capabilities=[
            ProviderCapability.OHLCV_DAILY,
            ProviderCapability.OHLCV_INTRADAY,
            ProviderCapability.ADJUSTED_CLOSE,
            ProviderCapability.SINGLE_SYMBOL,
            ProviderCapability.CACHE_READ,
            ProviderCapability.CACHE_WRITE
        ],
        requires_api_key=False,
        supports_offline=True,
        supports_bulk=False,
        supports_adjusted=True,
        notes=["Relies entirely on previously fetched data"]
    )

def local_fixture_capability_profile() -> ProviderCapabilityProfile:
    return ProviderCapabilityProfile(
        provider_name=DataProviderName.LOCAL_FIXTURE,
        provider_type=DataProviderType.LOCAL_FILE,
        capabilities=[
            ProviderCapability.OHLCV_DAILY,
            ProviderCapability.OHLCV_INTRADAY,
            ProviderCapability.SINGLE_SYMBOL,
            ProviderCapability.OFFLINE_FIXTURE
        ],
        requires_api_key=False,
        supports_offline=True,
        supports_bulk=False,
        supports_adjusted=True,
        notes=["For testing and regression harness only"]
    )

def manual_file_capability_profile() -> ProviderCapabilityProfile:
    return ProviderCapabilityProfile(
        provider_name=DataProviderName.MANUAL_FILE,
        provider_type=DataProviderType.LOCAL_FILE,
        capabilities=[
            ProviderCapability.OHLCV_DAILY,
            ProviderCapability.OHLCV_INTRADAY,
            ProviderCapability.SINGLE_SYMBOL
        ],
        requires_api_key=False,
        supports_offline=True,
        supports_bulk=False,
        supports_adjusted=True,
        notes=["Loads offline manual CSV/JSONL. Format must match OHLCV rules."]
    )

def synthetic_test_capability_profile() -> ProviderCapabilityProfile:
    return ProviderCapabilityProfile(
        provider_name=DataProviderName.SYNTHETIC_TEST,
        provider_type=DataProviderType.SYNTHETIC,
        capabilities=[
            ProviderCapability.OHLCV_DAILY,
            ProviderCapability.SINGLE_SYMBOL
        ],
        requires_api_key=False,
        supports_offline=True,
        supports_bulk=False,
        supports_adjusted=True,
        notes=["Used for testing."]
    )

def default_provider_capability_profiles() -> list[ProviderCapabilityProfile]:
    return [
        yfinance_capability_profile(),
        local_cache_capability_profile(),
        local_fixture_capability_profile(),
        manual_file_capability_profile(),
        synthetic_test_capability_profile()
    ]

def provider_supports_capability(profile: ProviderCapabilityProfile, capability: ProviderCapability) -> bool:
    return capability in profile.capabilities

def provider_supports_request(profile: ProviderCapabilityProfile, request: ProviderRequest) -> bool:
    if request.request_type == ProviderRequestType.OHLCV:
        if request.interval.endswith("m") or request.interval.endswith("h"):
            if not provider_supports_capability(profile, ProviderCapability.OHLCV_INTRADAY):
                return False
        else:
            if not provider_supports_capability(profile, ProviderCapability.OHLCV_DAILY):
                return False

        if len(request.symbols) > 1 and not profile.supports_bulk:
            return False

    elif request.request_type == ProviderRequestType.METADATA:
        if not provider_supports_capability(profile, ProviderCapability.SYMBOL_METADATA):
            return False
    elif request.request_type == ProviderRequestType.DIVIDENDS:
        if not provider_supports_capability(profile, ProviderCapability.DIVIDENDS):
            return False
    elif request.request_type == ProviderRequestType.SPLITS:
        if not provider_supports_capability(profile, ProviderCapability.SPLITS):
            return False

    return True

def capability_profiles_to_text(profiles: list[ProviderCapabilityProfile]) -> str:
    lines = ["--- Provider Capability Profiles ---"]
    for p in profiles:
        lines.append(f"Provider: {p.provider_name.value} ({p.provider_type.value})")
        lines.append(f"  Requires API Key: {p.requires_api_key}")
        lines.append(f"  Supports Offline: {p.supports_offline}")
        lines.append(f"  Supports Bulk: {p.supports_bulk}")
        lines.append(f"  Capabilities: {[c.value for c in p.capabilities]}")
        lines.append(f"  Notes: {', '.join(p.notes)}")
        lines.append("")
    return "\n".join(lines)
