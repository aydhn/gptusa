import abc
from typing import Any, Dict

from usa_signal_bot.data_providers.interfaces.base import DataProviderAdapterBase

class MarketDataProviderBase(DataProviderAdapterBase):
    @abc.abstractmethod
    def build_daily_ohlcv_plan(self, symbol: str, start_date: str | None = None, end_date: str | None = None) -> Any:
        pass

    @abc.abstractmethod
    def execute_metadata_only(self, request_or_plan: Any) -> Dict[str, Any]:
        pass

    @abc.abstractmethod
    def normalize_sample(self, payload: Any | None = None) -> Dict[str, Any]:
        pass
