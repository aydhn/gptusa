
from typing import Any
from usa_signal_bot.data_providers.interfaces.base import BaseDataProvider

class MacroDataProviderBase(BaseDataProvider):
    def build_macro_series_request(self, series_id: str) -> dict[str, Any]:
        return {"action": "macro_series", "series_id": series_id}

    def supported_series_metadata(self) -> list[dict[str, Any]]:
        return []

    def canonical_schema(self) -> list[str]:
        return []
