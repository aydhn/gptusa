
from usa_signal_bot.data_providers.interfaces.fundamentals import FundamentalDataProviderBase
from usa_signal_bot.core.enums import DataProviderName, DataProviderKind, DataProviderCapability

class SecCompanyFactsProviderSkeleton(FundamentalDataProviderBase):
    provider_name = DataProviderName.SEC_COMPANY_FACTS
    provider_kind = DataProviderKind.FUNDAMENTAL_DATA
    skeleton_only = True

    def capabilities(self) -> list[DataProviderCapability]:
        return []
