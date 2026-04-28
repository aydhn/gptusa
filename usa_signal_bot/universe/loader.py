import csv
from pathlib import Path
from typing import Optional, List, Dict, Any

from usa_signal_bot.universe.models import UniverseSymbol, UniverseDefinition, UniverseLoadResult
from usa_signal_bot.universe.schema import validate_universe_columns, normalize_universe_row
from usa_signal_bot.universe.symbols import normalize_symbol, normalize_asset_type, normalize_exchange, normalize_currency, parse_active
from usa_signal_bot.core.exceptions import UniverseLoadError, UniverseValidationError

def load_universe_csv(path: Path, universe_name: Optional[str] = None) -> UniverseLoadResult:
    if not path.exists() or not path.is_file():
        raise UniverseLoadError(f"Universe file not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise UniverseLoadError(f"Empty universe file: {path}")

            try:
                validate_universe_columns(reader.fieldnames)
            except UniverseValidationError as e:
                raise UniverseLoadError(f"Invalid columns in {path}: {e}")

            rows = list(reader)
            return load_universe_from_rows(rows, universe_name or path.stem, str(path))
    except Exception as e:
        if isinstance(e, UniverseLoadError):
            raise
        raise UniverseLoadError(f"Failed to read CSV {path}: {e}")

def load_universe_from_rows(rows: List[Dict[str, str]], universe_name: str, source_path: Optional[str] = None) -> UniverseLoadResult:
    valid_symbols = []
    seen_symbols = set()

    result = UniverseLoadResult(
        universe=UniverseDefinition(name=universe_name, created_from=source_path),
        source_path=source_path or "memory",
        row_count=len(rows)
    )

    for i, raw_row in enumerate(rows, start=1):
        try:
            norm_row = normalize_universe_row(raw_row)
            sym_str = normalize_symbol(norm_row.get("symbol", ""))

            if not sym_str:
                result.invalid_count += 1
                result.errors.append(f"Row {i}: Missing or empty symbol")
                continue

            from usa_signal_bot.universe.symbols import is_valid_symbol
            if not is_valid_symbol(sym_str):
                result.invalid_count += 1
                result.errors.append(f"Row {i}: Invalid symbol format '{sym_str}'")
                continue

            if sym_str in seen_symbols:
                result.duplicate_count += 1
                result.warnings.append(f"Row {i}: Duplicate symbol '{sym_str}' ignored")
                continue

            seen_symbols.add(sym_str)

            asset_type = normalize_asset_type(norm_row.get("asset_type", ""))

            symbol_obj = UniverseSymbol(
                symbol=sym_str,
                name=norm_row.get("name"),
                asset_type=asset_type,
                exchange=normalize_exchange(norm_row.get("exchange")),
                currency=normalize_currency(norm_row.get("currency")),
                active=parse_active(norm_row.get("active")),
                sector=norm_row.get("sector"),
                industry=norm_row.get("industry")
            )

            valid_symbols.append(symbol_obj)
            result.valid_count += 1

        except Exception as e:
            result.invalid_count += 1
            result.errors.append(f"Row {i}: {str(e)}")

    if not valid_symbols:
        raise UniverseValidationError(f"No valid symbols found in {source_path or 'rows'}")

    result.universe.symbols = valid_symbols
    return result

def load_default_watchlist(data_root: Path, watchlist_file: Optional[str] = None) -> UniverseLoadResult:
    if watchlist_file:
        file_path = Path(watchlist_file)
        if not file_path.is_absolute():
            file_path = data_root.parent / watchlist_file
    else:
        file_path = data_root / "universe" / "watchlist.csv"

    return load_universe_csv(file_path, "default_watchlist")

def save_universe_csv(path: Path, universe: UniverseDefinition) -> Path:
    from usa_signal_bot.universe.schema import ALL_UNIVERSE_COLUMNS

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ALL_UNIVERSE_COLUMNS)
        writer.writeheader()
        for sym in universe.symbols:
            row = {
                "symbol": sym.symbol,
                "asset_type": sym.asset_type.value if hasattr(sym.asset_type, 'value') else str(sym.asset_type),
                "name": sym.name or "",
                "exchange": sym.exchange or "",
                "currency": sym.currency,
                "active": "true" if sym.active else "false",
                "sector": sym.sector or "",
                "industry": sym.industry or "",
                "source": "",
                "notes": ""
            }
            writer.writerow(row)

    return path
