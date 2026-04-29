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
