
from usa_signal_bot.data_providers.interfaces.market_data import MarketDataProviderBase
from usa_signal_bot.core.enums import DataProviderName, DataProviderKind, DataProviderCapability

class StooqProviderSkeleton(MarketDataProviderBase):
    provider_name = DataProviderName.STOOQ
    provider_kind = DataProviderKind.MARKET_DATA
    skeleton_only = True

    def capabilities(self) -> list[DataProviderCapability]:
        return [
            DataProviderCapability.GET_DAILY_OHLCV,
            DataProviderCapability.GET_ADJUSTED_CLOSE,
            DataProviderCapability.GET_VOLUME,
            DataProviderCapability.GET_PROVIDER_HEALTH_METADATA,
        ]
