from pathlib import Path
from typing import List, Dict

from usa_signal_bot.universe.models import UniverseDefinition, UniverseSymbol
from usa_signal_bot.universe.loader import load_universe_csv, save_universe_csv
from usa_signal_bot.universe.registry import get_sample_stocks_path, get_sample_etfs_path, get_default_watchlist_path

def build_universe_from_files(paths: List[Path], name: str) -> UniverseDefinition:
    universes = []
    for p in paths:
        if p.exists() and p.is_file():
            res = load_universe_csv(p)
            universes.append(res.universe)

    return merge_universes(universes, name)

def merge_universes(universes: List[UniverseDefinition], name: str) -> UniverseDefinition:
    merged_symbols: Dict[str, UniverseSymbol] = {}

    for u in universes:
        for sym in u.symbols:
            if sym.symbol not in merged_symbols:
                merged_symbols[sym.symbol] = sym
            else:
                pass

    result = UniverseDefinition(
        name=name,
        symbols=list(merged_symbols.values()),
        created_from="merged"
    )
    return result

def build_default_universe(data_root: Path) -> UniverseDefinition:
    paths = [
        get_sample_stocks_path(data_root),
        get_sample_etfs_path(data_root),
        get_default_watchlist_path(data_root)
    ]
    return build_universe_from_files(paths, "default_universe")

def write_default_universe_snapshot(data_root: Path, universe: UniverseDefinition) -> Path:
    from usa_signal_bot.universe.registry import get_default_universe_snapshot_path
    snapshot_path = get_default_universe_snapshot_path(data_root)
    return save_universe_csv(snapshot_path, universe)
