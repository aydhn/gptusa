import copy
from typing import List, Optional

from usa_signal_bot.universe.models import UniverseDefinition, UniverseFilter
from usa_signal_bot.core.enums import AssetType
from usa_signal_bot.core.exceptions import UniverseValidationError

def filter_active_symbols(universe: UniverseDefinition) -> UniverseDefinition:
    new_universe = copy.deepcopy(universe)
    new_universe.symbols = [s for s in new_universe.symbols if s.active]
    return new_universe

def filter_by_asset_type(universe: UniverseDefinition, include_stocks: bool = True, include_etfs: bool = True) -> UniverseDefinition:
    if not include_stocks and not include_etfs:
        raise UniverseValidationError("Both include_stocks and include_etfs cannot be False")

    new_universe = copy.deepcopy(universe)
    valid_types = []
    if include_stocks:
        valid_types.append(AssetType.STOCK)
    if include_etfs:
        valid_types.append(AssetType.ETF)

    new_universe.symbols = [s for s in new_universe.symbols if s.asset_type in valid_types]
    return new_universe

def filter_by_exchange(universe: UniverseDefinition, exchanges: List[str]) -> UniverseDefinition:
    if not exchanges:
        return copy.deepcopy(universe)

    target_exchanges = [e.upper() for e in exchanges]
    new_universe = copy.deepcopy(universe)
    new_universe.symbols = [s for s in new_universe.symbols if s.exchange and s.exchange.upper() in target_exchanges]
    return new_universe

def limit_universe(universe: UniverseDefinition, max_symbols: Optional[int]) -> UniverseDefinition:
    if max_symbols is None:
        return copy.deepcopy(universe)

    if max_symbols <= 0:
        raise UniverseValidationError("max_symbols must be positive")

    new_universe = copy.deepcopy(universe)
    new_universe.symbols = new_universe.symbols[:max_symbols]
    return new_universe

def apply_universe_filter(universe: UniverseDefinition, universe_filter: UniverseFilter) -> UniverseDefinition:
    u = filter_by_asset_type(universe, universe_filter.include_stocks, universe_filter.include_etfs)
    u = filter_active_symbols(u) # Typically we only want active symbols when applying a filter
    u = limit_universe(u, universe_filter.max_symbols)
    return u
