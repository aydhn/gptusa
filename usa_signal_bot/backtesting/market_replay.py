"""Historical market data replay for the backtest engine."""
from dataclasses import dataclass, field
from typing import Any
from pathlib import Path
from datetime import datetime

from usa_signal_bot.core.enums import BacktestEventType
from usa_signal_bot.core.exceptions import BacktestMarketReplayError
from usa_signal_bot.data.models import OHLCVBar

import json
def load_jsonl(path):
    with open(path, 'r') as f:
        return [json.loads(line) for line in f if line.strip()]
from usa_signal_bot.backtesting.event_models import BacktestEvent, create_backtest_event

@dataclass
class MarketReplayRequest:
    symbols: list[str]
    timeframe: str
    provider_name: str = "yfinance"
    start_date: str | None = None
    end_date: str | None = None

@dataclass
class MarketReplayData:
    request: MarketReplayRequest
    bars_by_symbol: dict[str, list[OHLCVBar]]
    all_timestamps: list[str]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def filter_bars_by_date(bars: list[OHLCVBar], start_date: str | None, end_date: str | None) -> list[OHLCVBar]:
    filtered = []
    for bar in bars:
        dt = datetime.fromisoformat(bar.timestamp_utc.replace('Z', '+00:00'))
        if start_date:
            sd = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            if dt < sd:
                continue
        if end_date:
            ed = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            if dt > ed:
                continue
        filtered.append(bar)
    return filtered

def load_market_replay_data_from_cache(data_root: Path, request: MarketReplayRequest) -> MarketReplayData:
    bars_by_symbol: dict[str, list[OHLCVBar]] = {}
    timestamps_set = set()
    warnings = []
    errors = []

    for symbol in request.symbols:
        cache_dir = data_root / "cache" / request.provider_name / request.timeframe
        cache_file = cache_dir / f"{symbol}.jsonl"

        if not cache_file.exists():
            errors.append(f"Missing cache for {symbol} at {cache_file}")
            continue

        try:
            dicts = load_jsonl(cache_file)
            bars = [OHLCVBar(**d) for d in dicts]
            bars.sort(key=lambda x: x.timestamp_utc)
            bars = filter_bars_by_date(bars, request.start_date, request.end_date)

            bars_by_symbol[symbol] = bars
            for b in bars:
                timestamps_set.add(b.timestamp_utc)
        except Exception as e:
            errors.append(f"Failed to load cache for {symbol}: {e}")

    all_timestamps = sorted(list(timestamps_set))

    if not bars_by_symbol:
        warnings.append("No market data loaded from cache.")

    return MarketReplayData(
        request=request,
        bars_by_symbol=bars_by_symbol,
        all_timestamps=all_timestamps,
        warnings=warnings,
        errors=errors
    )

def build_market_bar_events(data: MarketReplayData) -> list[BacktestEvent]:
    events = []
    for symbol, bars in data.bars_by_symbol.items():
        for i, bar in enumerate(bars):
            payload = {
                "open": bar.open,
                "high": bar.high,
                "low": bar.low,
                "close": bar.close,
                "volume": bar.volume,
                "is_closed": True
            }
            event = create_backtest_event(
                event_type=BacktestEventType.MARKET_BAR,
                timestamp_utc=bar.timestamp_utc,
                symbol=symbol,
                timeframe=data.request.timeframe,
                payload=payload,
                sequence=0
            )
            events.append(event)
    return events

def get_bar_by_symbol_time(data: MarketReplayData, symbol: str, timestamp_utc: str) -> OHLCVBar | None:
    bars = data.bars_by_symbol.get(symbol, [])
    for bar in bars:
        if bar.timestamp_utc == timestamp_utc:
            return bar
    return None

def get_next_bar_for_symbol(data: MarketReplayData, symbol: str, timestamp_utc: str) -> OHLCVBar | None:
    bars = data.bars_by_symbol.get(symbol, [])
    for bar in bars:
        if bar.timestamp_utc > timestamp_utc:
            return bar
    return None

def validate_market_replay_data(data: MarketReplayData) -> None:
    if data.errors:
        if not data.bars_by_symbol:
            raise BacktestMarketReplayError(f"No market data could be loaded. Errors: {data.errors}")
