import re
from typing import List, Optional

from usa_signal_bot.core.enums import AssetType
from usa_signal_bot.core.exceptions import SymbolValidationError

SYMBOL_PATTERN = re.compile(r'^[A-Z0-9\.\-]+$')
MAX_SYMBOL_LENGTH = 15

def normalize_symbol(symbol: str) -> str:
    if not symbol:
        return ""
    return symbol.strip().upper()

def is_valid_symbol(symbol: str, max_length: int = MAX_SYMBOL_LENGTH) -> bool:
    if not symbol:
        return False
    if len(symbol) > max_length:
        return False
    if not SYMBOL_PATTERN.match(symbol):
        return False
    return True

def validate_symbol(symbol: str, max_length: int = MAX_SYMBOL_LENGTH) -> None:
    if not symbol:
        raise SymbolValidationError("Symbol cannot be empty.")
    if len(symbol) > max_length:
        raise SymbolValidationError(f"Symbol '{symbol}' exceeds maximum length of {max_length}.")
    if not SYMBOL_PATTERN.match(symbol):
        raise SymbolValidationError(f"Symbol '{symbol}' contains invalid characters. Only A-Z, 0-9, ., - are allowed.")

def normalize_asset_type(asset_type: str) -> AssetType:
    try:
        if not asset_type:
            return AssetType.STOCK
        return AssetType(asset_type.strip().upper())
    except ValueError:
        raise SymbolValidationError(f"Invalid asset type: '{asset_type}'. Must be 'STOCK' or 'ETF'.")

def normalize_exchange(exchange: Optional[str]) -> Optional[str]:
    if not exchange:
        return None
    return exchange.strip().upper()

def normalize_currency(currency: Optional[str]) -> str:
    from usa_signal_bot.universe.schema import DEFAULT_CURRENCY
    if not currency:
        return DEFAULT_CURRENCY
    return currency.strip().upper()

def parse_active(value: str | bool | None) -> bool:
    if value is None:
        return True
    if isinstance(value, bool):
        return value
    val_str = str(value).strip().lower()
    if not val_str:
        return True
    return val_str in ("true", "1", "yes", "y", "t", "active")

def sort_symbols(symbols: List[str]) -> List[str]:
    return sorted(symbols)

def deduplicate_symbols(symbols: List[str]) -> List[str]:
    seen = set()
    result = []
    for s in symbols:
        if s not in seen:
            seen.add(s)
            result.append(s)
    return result
