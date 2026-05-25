
from typing import Any
from usa_signal_bot.data_providers.interfaces.base import BaseDataProvider

class FundamentalDataProviderBase(BaseDataProvider):
    def build_company_profile_request(self, symbol: str) -> dict[str, Any]:
        return {"action": "company_profile", "symbol": symbol}

    def build_fundamentals_request(self, symbol: str) -> dict[str, Any]:
        return {"action": "fundamentals", "symbol": symbol}

    def canonical_schema(self) -> list[str]:
        return []
