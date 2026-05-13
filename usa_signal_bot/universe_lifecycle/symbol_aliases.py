from pathlib import Path
from typing import Any, List, Optional, Dict
import json

from usa_signal_bot.core.enums import SymbolAliasType, SymbolLifecycleSource
from usa_signal_bot.universe_lifecycle.lifecycle_models import (
    SymbolAliasRecord, validate_symbol_alias_record, create_symbol_alias_id
)
from usa_signal_bot.core.exceptions import SymbolAliasError

def load_symbol_aliases(path: Path) -> List[SymbolAliasRecord]:
    if not path.exists() or not path.is_file():
        return []
    aliases = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            record = SymbolAliasRecord(
                alias_id=item.get("alias_id") or create_symbol_alias_id(item.get("old_symbol", ""), item.get("new_symbol", "")),
                old_symbol=item.get("old_symbol", "").upper(),
                new_symbol=item.get("new_symbol", "").upper(),
                alias_type=SymbolAliasType(item.get("alias_type", SymbolAliasType.UNKNOWN.value)),
                effective_date=item.get("effective_date"),
                source=SymbolLifecycleSource(item.get("source", SymbolLifecycleSource.MANUAL_REGISTRY.value)),
                confidence=item.get("confidence"),
                notes=item.get("notes", [])
            )
            validate_symbol_alias_record(record)
            aliases.append(record)
        return aliases
    except Exception as e:
        raise SymbolAliasError(f"Failed to load symbol aliases from {path}: {e}")

def write_symbol_aliases_example(path: Path) -> Path:
    from usa_signal_bot.universe_lifecycle.lifecycle_models import symbol_alias_record_to_dict
    aliases = [
        SymbolAliasRecord(
            alias_id=create_symbol_alias_id("FB", "META"),
            old_symbol="FB",
            new_symbol="META",
            alias_type=SymbolAliasType.TICKER_CHANGE,
            effective_date="2022-06-09"
        ),
        SymbolAliasRecord(
            alias_id=create_symbol_alias_id("SQ", "BLOCK"),
            old_symbol="SQ",
            new_symbol="BLOCK",
            alias_type=SymbolAliasType.TICKER_CHANGE,
            effective_date="2021-12-10"
        )
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([symbol_alias_record_to_dict(a) for a in aliases], f, indent=2)
    return path

def alias_for_old_symbol(aliases: List[SymbolAliasRecord], symbol: str) -> Optional[SymbolAliasRecord]:
    sym = symbol.upper()
    for a in aliases:
        if a.old_symbol == sym:
            return a
    return None

def aliases_for_symbol(aliases: List[SymbolAliasRecord], symbol: str) -> List[SymbolAliasRecord]:
    sym = symbol.upper()
    return [a for a in aliases if a.old_symbol == sym or a.new_symbol == sym]

def resolve_symbol_alias(symbol: str, aliases: List[SymbolAliasRecord], as_of_date: Optional[str] = None) -> str:
    current = symbol.upper()
    visited = set()
    while current not in visited:
        visited.add(current)
        alias = alias_for_old_symbol(aliases, current)
        if not alias:
            break
        if as_of_date and alias.effective_date and alias.effective_date > as_of_date:
            break
        current = alias.new_symbol
    return current

def apply_aliases_to_symbols(symbols: List[str], aliases: List[SymbolAliasRecord], as_of_date: Optional[str] = None) -> List[str]:
    return [resolve_symbol_alias(s, aliases, as_of_date) for s in symbols]

def symbol_aliases_to_text(aliases: List[SymbolAliasRecord], limit: int = 100) -> str:
    lines = [f"Symbol Aliases Registry ({len(aliases)} records)"]
    lines.append("Note: Alias resolution results carry no absolute certainty.")
    count = 0
    for a in aliases:
        if count >= limit:
            lines.append(f"... and {len(aliases) - limit} more.")
            break
        eff_str = f" [Effective: {a.effective_date}]" if a.effective_date else ""
        lines.append(f" - {a.old_symbol} -> {a.new_symbol} ({a.alias_type.value}){eff_str}")
        count += 1
    return "\n".join(lines)
