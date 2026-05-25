
from usa_signal_bot.data_providers.interfaces.market_data import MarketDataProviderBase
from usa_signal_bot.core.enums import DataProviderName, DataProviderKind, DataProviderCapability

class LocalCsvProviderSkeleton(MarketDataProviderBase):
    provider_name = DataProviderName.LOCAL_CSV
    provider_kind = DataProviderKind.LOCAL_FIXTURE
    skeleton_only = True

    def capabilities(self) -> list[DataProviderCapability]:
        return [
            DataProviderCapability.READ_LOCAL_FIXTURE,
            DataProviderCapability.VALIDATE_SCHEMA,
            DataProviderCapability.NORMALIZE_RESPONSE,
            DataProviderCapability.GET_PROVIDER_HEALTH_METADATA,
        ]
