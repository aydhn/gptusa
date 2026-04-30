from typing import Any
import math
from typing import List
from usa_signal_bot.core.exceptions import DataValidationError

def validate_batch_size(batch_size: int) -> None:
    if not isinstance(batch_size, int) or batch_size <= 0:
        raise DataValidationError("batch_size must be a positive integer.")

def chunk_symbols(symbols: List[str], batch_size: int) -> List[List[str]]:
    """Splits a list of symbols into chunks of batch_size."""
    if not symbols:
        return []
    validate_batch_size(batch_size)
    return [symbols[i:i + batch_size] for i in range(0, len(symbols), batch_size)]

def estimate_batch_count(symbols: List[str], batch_size: int) -> int:
    """Estimates the number of batches required."""
    if not symbols:
        return 0
    validate_batch_size(batch_size)
    return math.ceil(len(symbols) / batch_size)

def build_symbol_batches(symbols: List[str], batch_size: int, deduplicate: bool = True) -> List[List[str]]:
    """Cleans, optionally deduplicates, and splits symbols into batches while preserving order."""
    if not symbols:
        return []

    cleaned_symbols = []
    seen = set()

    for sym in symbols:
        if not sym or not isinstance(sym, str):
             continue
        s = sym.strip().upper()
        if not s:
             continue
        if deduplicate:
            if s not in seen:
                seen.add(s)
                cleaned_symbols.append(s)
        else:
            cleaned_symbols.append(s)

    return chunk_symbols(cleaned_symbols, batch_size)

from dataclasses import dataclass

@dataclass
class SymbolBatch:
    batch_id: str
    symbols: list[str]
    index: int
    total_batches: int

def build_symbol_batch_objects(symbols: list[str], batch_size: int):
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")

    batches = []
    total = (len(symbols) + batch_size - 1) // batch_size

    for i in range(total):
        start = i * batch_size
        end = min(start + batch_size, len(symbols))
        batch_symbols = symbols[start:end]

        batches.append(SymbolBatch(
            batch_id=f"batch_{i+1:04d}_{total:04d}",
            symbols=batch_symbols,
            index=i,
            total_batches=total
        ))

    return batches

def symbol_batch_to_text(batch: SymbolBatch) -> str:
    return f"Batch {batch.batch_id} [{batch.index + 1}/{batch.total_batches}] with {len(batch.symbols)} symbols"

def estimate_large_universe_runtime(symbol_count: int, timeframe_count: int, min_seconds_between_requests: float, batch_size: int) -> dict[str, Any]:
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")

    total_requests = symbol_count * timeframe_count
    total_wait_time = total_requests * min_seconds_between_requests
    total_batches = (symbol_count + batch_size - 1) // batch_size

    estimated_download_time = total_requests * 2.0
    total_estimated_seconds = total_wait_time + estimated_download_time

    return {
        "symbol_count": symbol_count,
        "timeframe_count": timeframe_count,
        "total_requests": total_requests,
        "total_batches": total_batches,
        "estimated_wait_time_seconds": total_wait_time,
        "estimated_download_time_seconds": estimated_download_time,
        "total_estimated_seconds": total_estimated_seconds,
        "total_estimated_minutes": total_estimated_seconds / 60.0,
        "total_estimated_hours": total_estimated_seconds / 3600.0
    }
