from pathlib import Path
from typing import List

def list_universe_files(data_root: Path) -> List[Path]:
    universe_dir = data_root / "universe"
    if not universe_dir.exists() or not universe_dir.is_dir():
        return []

    files = []
    for p in universe_dir.glob("*.csv"):
        if p.is_file():
            files.append(p)

    return sorted(files)

def get_default_watchlist_path(data_root: Path) -> Path:
    return data_root / "universe" / "watchlist.csv"

def get_sample_stocks_path(data_root: Path) -> Path:
    return data_root / "universe" / "sample_stocks.csv"

def get_sample_etfs_path(data_root: Path) -> Path:
    return data_root / "universe" / "sample_etfs.csv"

def get_default_universe_snapshot_path(data_root: Path) -> Path:
    return data_root / "universe" / "default_universe.csv"
