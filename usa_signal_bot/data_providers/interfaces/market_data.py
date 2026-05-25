
from typing import Any
from usa_signal_bot.data_providers.interfaces.base import BaseDataProvider

class MarketDataProviderBase(BaseDataProvider):
    def build_daily_ohlcv_request(self, symbol: str) -> dict[str, Any]:
        return {"action": "daily_ohlcv", "symbol": symbol}

    def build_intraday_ohlcv_request(self, symbol: str, interval: str) -> dict[str, Any]:
        return {"action": "intraday_ohlcv", "symbol": symbol, "interval": interval}

    def supported_intervals(self) -> list[str]:
        return ["1m", "5m", "15m", "1d"]

    def canonical_schema(self) -> list[str]:
        return ["symbol", "timestamp", "open", "high", "low", "close", "adjusted_close", "volume", "source", "fetched_at_utc", "quality_flags"]
