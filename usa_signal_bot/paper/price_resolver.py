from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from pathlib import Path
from datetime import datetime, timezone

from usa_signal_bot.core.enums import PaperOrderType
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.data.cache import find_latest_cache_file, read_cached_ohlcv_bars

@dataclass
class PaperPriceSnapshot:
    symbol: str
    timeframe: str
    timestamp_utc: str
    price: float
    source: str
    metadata: Dict[str, Any] = field(default_factory=dict)

class LocalPriceResolver:
    """
    Resolves local prices for paper trading.
    Strictly reads from local cache. DOES NOT fetch from internet.
    """
    def __init__(self, data_root: Path, provider_name: str = "yfinance"):
        self.data_root = data_root
        self.provider_name = provider_name

    def _read_cache(self, symbol: str, timeframe: str) -> List[OHLCVBar]:
        latest_file = find_latest_cache_file(self.data_root, self.provider_name, symbol, timeframe)
        if not latest_file:
            return []
        try:
            return read_cached_ohlcv_bars(latest_file)
        except Exception:
            return []

    def resolve_latest_price(self, symbol: str, timeframe: str = "1d") -> Optional[PaperPriceSnapshot]:
        bars = self._read_cache(symbol, timeframe)
        if not bars:
            return None

        latest_bar = sorted(bars, key=lambda b: b.timestamp_utc)[-1]

        # Prefer adjusted close if available
        price = latest_bar.adj_close if latest_bar.adj_close is not None else latest_bar.close

        return PaperPriceSnapshot(
            symbol=symbol,
            timeframe=timeframe,
            timestamp_utc=latest_bar.timestamp_utc,
            price=price,
            source="local_cache",
            metadata={"bar": latest_bar.__dict__}
        )

    def resolve_price_at_or_after(self, symbol: str, timestamp_utc: str, timeframe: str = "1d") -> Optional[PaperPriceSnapshot]:
        bars = self._read_cache(symbol, timeframe)
        if not bars:
            return None

        sorted_bars = sorted(bars, key=lambda b: b.timestamp_utc)
        for bar in sorted_bars:
            if bar.timestamp_utc >= timestamp_utc:
                price = bar.adj_close if bar.adj_close is not None else bar.close
                return PaperPriceSnapshot(
                    symbol=symbol,
                    timeframe=timeframe,
                    timestamp_utc=bar.timestamp_utc,
                    price=price,
                    source="local_cache",
                    metadata={"bar": bar.__dict__}
                )

        # If no bar after timestamp, maybe fallback to latest?
        return self.resolve_latest_price(symbol, timeframe)

    def resolve_bar_for_order(self, symbol: str, timeframe: str, order_type: PaperOrderType, timestamp_utc: Optional[str] = None) -> Optional[OHLCVBar]:
        bars = self._read_cache(symbol, timeframe)
        if not bars:
            return None

        sorted_bars = sorted(bars, key=lambda b: b.timestamp_utc)

        if timestamp_utc:
            for bar in sorted_bars:
                if bar.timestamp_utc >= timestamp_utc:
                    return bar

        # Fallback to latest
        return sorted_bars[-1]

    def resolve_many_latest(self, symbols: List[str], timeframe: str = "1d") -> Dict[str, PaperPriceSnapshot]:
        res = {}
        for sym in symbols:
            snap = self.resolve_latest_price(sym, timeframe)
            if snap:
                res[sym] = snap
        return res
