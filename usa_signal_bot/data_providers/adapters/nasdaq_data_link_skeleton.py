
from usa_signal_bot.data_providers.interfaces.fundamentals import FundamentalDataProviderBase
from usa_signal_bot.core.enums import DataProviderName, DataProviderKind, DataProviderCapability

class NasdaqDataLinkFreeProviderSkeleton(FundamentalDataProviderBase):
    provider_name = DataProviderName.NASDAQ_DATA_LINK_FREE
    provider_kind = DataProviderKind.FUNDAMENTAL_DATA
    skeleton_only = True

    def capabilities(self) -> list[DataProviderCapability]:
        return []
