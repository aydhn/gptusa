
from typing import Any
from usa_signal_bot.data_providers.interfaces.base import BaseDataProvider

class NewsMetadataProviderBase(BaseDataProvider):
    def build_news_metadata_request(self, symbol: str | None = None) -> dict[str, Any]:
        return {"action": "news_metadata", "symbol": symbol}

    def canonical_schema(self) -> list[str]:
        return []
