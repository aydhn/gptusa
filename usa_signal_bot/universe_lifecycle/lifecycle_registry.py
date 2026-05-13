from pathlib import Path
from typing import Any, List, Optional, Dict
import json

from usa_signal_bot.core.enums import SymbolLifecycleStatus, SymbolLifecycleSource
from usa_signal_bot.universe_lifecycle.lifecycle_models import (
    SymbolLifecycleRecord, validate_symbol_lifecycle_record
)
from usa_signal_bot.universe_lifecycle.universe_snapshot import UniverseSnapshot
from usa_signal_bot.core.exceptions import LifecycleRegistryError

def load_lifecycle_registry(path: Path) -> List[SymbolLifecycleRecord]:
    if not path.exists() or not path.is_file():
        return []
    records = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            record = SymbolLifecycleRecord(
                symbol=item.get("symbol", "").upper(),
                status=SymbolLifecycleStatus(item.get("status", SymbolLifecycleStatus.UNKNOWN.value)),
                source=SymbolLifecycleSource(item.get("source", SymbolLifecycleSource.MANUAL_REGISTRY.value)),
                first_seen_date=item.get("first_seen_date"),
                last_seen_date=item.get("last_seen_date"),
                listed_date=item.get("listed_date"),
                delisted_date=item.get("delisted_date"),
                successor_symbol=item.get("successor_symbol"),
                predecessor_symbol=item.get("predecessor_symbol"),
                reason=item.get("reason"),
                confidence=item.get("confidence"),
                notes=item.get("notes", []),
                metadata=item.get("metadata", {})
            )
            validate_symbol_lifecycle_record(record)
            records.append(record)
        return merge_lifecycle_records(records, [])
    except Exception as e:
        raise LifecycleRegistryError(f"Failed to load lifecycle registry from {path}: {e}")

def write_lifecycle_registry_example(path: Path) -> Path:
    from usa_signal_bot.universe_lifecycle.lifecycle_models import symbol_lifecycle_record_to_dict
    records = [
        SymbolLifecycleRecord(
            symbol="SPY",
            status=SymbolLifecycleStatus.ACTIVE,
            source=SymbolLifecycleSource.MANUAL_REGISTRY,
            listed_date="1993-01-22"
        ),
        SymbolLifecycleRecord(
            symbol="TWTR",
            status=SymbolLifecycleStatus.ACQUIRED,
            source=SymbolLifecycleSource.MANUAL_REGISTRY,
            delisted_date="2022-10-28",
            reason="Acquired by Elon Musk"
        )
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([symbol_lifecycle_record_to_dict(r) for r in records], f, indent=2)
    return path

def merge_lifecycle_records(primary: List[SymbolLifecycleRecord], secondary: List[SymbolLifecycleRecord]) -> List[SymbolLifecycleRecord]:
    merged: Dict[str, SymbolLifecycleRecord] = {}
    for r in secondary:
        merged[r.symbol] = r
    for r in primary:
        merged[r.symbol] = r
    return list(merged.values())

def lifecycle_record_for_symbol(records: List[SymbolLifecycleRecord], symbol: str) -> Optional[SymbolLifecycleRecord]:
    sym = symbol.upper()
    for r in records:
        if r.symbol == sym:
            return r
    return None

def lifecycle_records_for_symbols(records: List[SymbolLifecycleRecord], symbols: List[str]) -> List[SymbolLifecycleRecord]:
    target_symbols = set(s.upper() for s in symbols)
    return [r for r in records if r.symbol in target_symbols]

def infer_lifecycle_records_from_snapshots(snapshots: List[UniverseSnapshot]) -> List[SymbolLifecycleRecord]:
    if not snapshots:
        return []
    valid_snapshots = [s for s in snapshots if s.as_of_date]
    sorted_snapshots = sorted(valid_snapshots, key=lambda s: s.as_of_date)
    symbol_first_seen: Dict[str, str] = {}
    symbol_last_seen: Dict[str, str] = {}
    for s in sorted_snapshots:
        for sym in s.symbols:
            if sym not in symbol_first_seen:
                symbol_first_seen[sym] = s.as_of_date
            symbol_last_seen[sym] = s.as_of_date
    records = []
    latest_date = sorted_snapshots[-1].as_of_date
    for sym, first in symbol_first_seen.items():
        last = symbol_last_seen[sym]
        status = SymbolLifecycleStatus.ACTIVE
        if last < latest_date:
            status = SymbolLifecycleStatus.INACTIVE
        records.append(SymbolLifecycleRecord(
            symbol=sym,
            status=status,
            source=SymbolLifecycleSource.INFERRED_FROM_HISTORY,
            first_seen_date=first,
            last_seen_date=last,
            confidence=0.5,
            notes=["Inferred from universe snapshots"]
        ))
    return records

def lifecycle_registry_to_text(records: List[SymbolLifecycleRecord], limit: int = 100) -> str:
    lines = [f"Lifecycle Registry ({len(records)} records)"]
    lines.append("Note: Manual registry is not a guarantee of accurate historical data.")
    count = 0
    for r in records:
        if count >= limit:
            lines.append(f"... and {len(records) - limit} more.")
            break
        delist_str = f" [Delisted: {r.delisted_date}]" if r.delisted_date else ""
        lines.append(f" - {r.symbol}: {r.status.value}{delist_str} (Source: {r.source.value})")
        count += 1
    return "\n".join(lines)
