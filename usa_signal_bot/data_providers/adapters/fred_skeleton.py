
from usa_signal_bot.data_providers.interfaces.macro import MacroDataProviderBase
from usa_signal_bot.core.enums import DataProviderName, DataProviderKind, DataProviderCapability

class FredCompatibleProviderSkeleton(MacroDataProviderBase):
    provider_name = DataProviderName.FRED_COMPATIBLE
    provider_kind = DataProviderKind.MACRO_DATA
    skeleton_only = True

    def capabilities(self) -> list[DataProviderCapability]:
        return []
