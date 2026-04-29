import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Any
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

def list_market_data_cache_files(data_root: Path) -> List[Path]:
    """Lists all JSONL files in the market data cache directory."""
    cache_dir = market_data_cache_dir(data_root)
    if not cache_dir.exists():
        return []
    return list(cache_dir.glob("*.jsonl"))

def cache_file_age_seconds(path: Path) -> Optional[float]:
    """Returns the age of a cache file in seconds, or None if it doesn't exist."""
    if not path.exists():
        return None
    return time.time() - path.stat().st_mtime

def cache_file_size(path: Path) -> Optional[int]:
    """Returns the size of a cache file in bytes, or None if it doesn't exist."""
    if not path.exists():
        return None
    return path.stat().st_size

def validate_cache_file(path: Path, expected_symbols: Optional[List[str]] = None) -> 'DataQualityReport':
    """Validates the contents of a cache file and returns a DataQualityReport."""
    from usa_signal_bot.data.quality import run_full_ohlcv_quality_validation
    from usa_signal_bot.data.models import OHLCVBar
    from usa_signal_bot.core.exceptions import DataCacheError

    try:
        raw_bars = read_ohlcv_bars_cache(path)
        bars = [OHLCVBar(**b) for b in raw_bars]
    except Exception as e:
        raise DataCacheError(f"Corrupt cache file {path}: {e}")

    # Extract provider and timeframe from filename
    # e.g., mock_SPY_1h_start_end.jsonl
    parts = path.name.split('_')
    provider = parts[0] if len(parts) > 0 else "unknown"
    timeframe = parts[2] if len(parts) > 2 else "unknown"

    symbols_to_check = expected_symbols if expected_symbols else list(set(b.symbol for b in bars))
    report, _ = run_full_ohlcv_quality_validation(bars, symbols_to_check, provider, timeframe)
    return report

def read_cached_ohlcv_bars(path: Path) -> List[OHLCVBar]:
    """Reads a cache file and returns a list of OHLCVBar objects."""
    raw_bars = read_ohlcv_bars_cache(path)
    return [OHLCVBar(**b) for b in raw_bars]

def write_repaired_cache(path: Path, bars: List[OHLCVBar]) -> Path:
    """Writes repaired bars to cache."""
    return write_ohlcv_bars_cache(path, bars)

def cache_summary(data_root: Path) -> Dict[str, Any]:
    """Returns a summary of the market data cache."""
    files = list_market_data_cache_files(data_root)
    count = len(files)
    total_size = sum(cache_file_size(f) or 0 for f in files)

    newest = None
    oldest = None

    if files:
        sorted_files = sorted(files, key=lambda f: f.stat().st_mtime)
        newest = sorted_files[-1].name
        oldest = sorted_files[0].name

    return {
        "file_count": count,
        "total_size_bytes": total_size,
        "newest_file": newest,
        "oldest_file": oldest
    }

def list_cache_files_for_timeframe(data_root: Path, timeframe: str) -> list[Path]:
    cache_dir = market_data_cache_dir(data_root)
    if not cache_dir.exists():
        return []
    # format: yfinance_AAPL_1d.jsonl or yfinance_AAPL_1d_20230101.jsonl
    return list(cache_dir.glob(f"*_{timeframe}.jsonl")) + list(cache_dir.glob(f"*_{timeframe}_*.jsonl"))

def list_cache_files_for_symbol(data_root: Path, symbol: str) -> list[Path]:
    cache_dir = market_data_cache_dir(data_root)
    if not cache_dir.exists():
        return []
    return list(cache_dir.glob(f"*_{symbol}_*.jsonl"))

def find_latest_cache_file(data_root: Path, provider_name: str, symbol: str, timeframe: str) -> Optional[Path]:
    cache_dir = market_data_cache_dir(data_root)
    if not cache_dir.exists():
        return None
    # match specific pattern to avoid collisions
    pattern = f"{provider_name}_{symbol}_{timeframe}*.jsonl"
    files = list(cache_dir.glob(pattern))
    if not files:
        return None
    return sorted(files, key=lambda x: x.stat().st_mtime)[-1]

def read_cached_bars_for_symbols_timeframe(data_root: Path, symbols: list[str], timeframe: str, provider_name: str = "yfinance") -> list[OHLCVBar]:
    all_bars = []
    for sym in symbols:
        latest = find_latest_cache_file(data_root, provider_name, sym, timeframe)
        if latest:
            try:
                raw_bars = read_ohlcv_bars_cache(latest)
                for b in raw_bars:
                    all_bars.append(OHLCVBar(**b))
            except Exception:
                pass
    return all_bars

def market_data_cache_summary_by_timeframe(data_root: Path) -> dict[str, Any]:
    cache_dir = market_data_cache_dir(data_root)
    summary = {}
    if not cache_dir.exists():
        return summary

    files = list_market_data_cache_files(data_root)
    for f in files:
        parts = f.stem.split('_')
        if len(parts) >= 3:
            tf = parts[2]
            if tf not in summary:
                summary[tf] = {"count": 0, "size_bytes": 0}
            summary[tf]["count"] += 1
            summary[tf]["size_bytes"] += f.stat().st_size

    return summary
