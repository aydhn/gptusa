
from typing import Any
from usa_signal_bot.data_providers.interfaces.base import BaseDataProvider

class CalendarDataProviderBase(BaseDataProvider):
    def build_earnings_calendar_request(self, symbol: str | None = None) -> dict[str, Any]:
        return {"action": "earnings_calendar", "symbol": symbol}

    def build_market_calendar_request(self) -> dict[str, Any]:
        return {"action": "market_calendar"}

    def canonical_schema(self) -> list[str]:
        return []
