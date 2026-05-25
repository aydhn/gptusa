
from typing import Any
from usa_signal_bot.data_providers.interfaces.base import BaseDataProvider
from usa_signal_bot.core.enums import ProviderDataDomain

class SymbolUniverseProviderBase(BaseDataProvider):
    def build_symbol_universe_request(self, domain: ProviderDataDomain) -> dict[str, Any]:
        return {"action": "symbol_universe", "domain": domain}

    def canonical_schema(self) -> list[str]:
        return []
