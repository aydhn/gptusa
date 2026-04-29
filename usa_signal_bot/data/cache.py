import json
import time
from pathlib import Path
from typing import List, Dict, Optional
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.utils.text_utils import clean_symbol_for_filename
from usa_signal_bot.utils.file_utils import safe_mkdir

def market_data_cache_dir(data_root: Path) -> Path:
    """Returns the market data cache directory, ensuring it exists."""
    cache_dir = data_root / "cache" / "market_data"
    safe_mkdir(cache_dir)
    return cache_dir

def build_market_data_cache_filename(provider_name: str, symbol: str, timeframe: str, start_date: Optional[str], end_date: Optional[str]) -> str:
    """Builds a deterministic filename for a cache entry."""
    safe_symbol = clean_symbol_for_filename(symbol)
    start_str = start_date.replace("-", "") if start_date else "start"
    end_str = end_date.replace("-", "") if end_date else "end"
    # To keep it deterministic but concise, we include provider, symbol, timeframe, start, end
    return f"{provider_name}_{safe_symbol}_{timeframe}_{start_str}_{end_str}.jsonl"

def build_market_data_cache_path(data_root: Path, provider_name: str, symbol: str, timeframe: str, start_date: Optional[str], end_date: Optional[str]) -> Path:
    """Builds the full Path for a cache entry."""
    filename = build_market_data_cache_filename(provider_name, symbol, timeframe, start_date, end_date)
    return market_data_cache_dir(data_root) / filename

def write_ohlcv_bars_cache(path: Path, bars: List[OHLCVBar]) -> Path:
    """Writes a list of OHLCVBars to a JSONL cache file."""
    # Ensure parent dir exists
    safe_mkdir(path.parent)

    with path.open('w', encoding='utf-8') as f:
        for bar in bars:
            f.write(json.dumps(bar.to_dict()) + '\n')
    return path

def read_ohlcv_bars_cache(path: Path) -> List[dict]:
    """Reads a JSONL cache file into a list of dicts. Conversion to OHLCVBar happens downstream if needed."""
    bars_data = []
    if not path.exists():
        return bars_data

    with path.open('r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                bars_data.append(json.loads(line))
    return bars_data

def cache_exists(path: Path) -> bool:
    """Checks if a cache file exists and is not empty."""
    return path.exists() and path.stat().st_size > 0

def is_cache_fresh(path: Path, ttl_seconds: int) -> bool:
    """Checks if a cache file is fresher than ttl_seconds."""
    if not cache_exists(path):
        return False
    mtime = path.stat().st_mtime
    age = time.time() - mtime
    return age < ttl_seconds

def split_bars_by_symbol(bars: List[OHLCVBar]) -> Dict[str, List[OHLCVBar]]:
    """Helper to split a mixed list of bars into a dict grouped by symbol."""
    grouped = {}
    for bar in bars:
        if bar.symbol not in grouped:
            grouped[bar.symbol] = []
        grouped[bar.symbol].append(bar)
    return grouped
