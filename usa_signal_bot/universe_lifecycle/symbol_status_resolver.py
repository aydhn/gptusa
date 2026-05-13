from typing import List, Optional

from usa_signal_bot.core.enums import SymbolLifecycleStatus, SymbolLifecycleSource
from usa_signal_bot.universe_lifecycle.lifecycle_models import SymbolLifecycleRecord, SymbolAliasRecord
from usa_signal_bot.universe_lifecycle.lifecycle_registry import lifecycle_record_for_symbol
from usa_signal_bot.universe_lifecycle.symbol_aliases import alias_for_old_symbol, aliases_for_symbol

class SymbolStatusResolver:
    def __init__(self, lifecycle_records: Optional[List[SymbolLifecycleRecord]] = None, aliases: Optional[List[SymbolAliasRecord]] = None):
        self.lifecycle_records = lifecycle_records or []
        self.aliases = aliases or []

    def resolve_status(self, symbol: str, as_of_date: Optional[str] = None) -> SymbolLifecycleRecord:
        sym = symbol.upper()
        record = lifecycle_record_for_symbol(self.lifecycle_records, sym)
        if not record:
            return SymbolLifecycleRecord(
                symbol=sym,
                status=SymbolLifecycleStatus.UNKNOWN,
                source=SymbolLifecycleSource.UNKNOWN,
                notes=["Symbol not found in registry. Review required."]
            )
        status = record.status
        if as_of_date:
            if record.listed_date and record.listed_date > as_of_date:
                status = SymbolLifecycleStatus.INACTIVE
                record.notes.append(f"Listed date {record.listed_date} is in the future relative to {as_of_date}")
            elif record.delisted_date and record.delisted_date <= as_of_date:
                status = SymbolLifecycleStatus.DELISTED
            elif status == SymbolLifecycleStatus.DELISTED and (not record.delisted_date or record.delisted_date > as_of_date):
                status = SymbolLifecycleStatus.ACTIVE
        return SymbolLifecycleRecord(
            symbol=record.symbol,
            status=status,
            source=record.source,
            first_seen_date=record.first_seen_date,
            last_seen_date=record.last_seen_date,
            listed_date=record.listed_date,
            delisted_date=record.delisted_date,
            successor_symbol=record.successor_symbol or self.resolve_successor(sym, as_of_date),
            predecessor_symbol=record.predecessor_symbol or self.resolve_predecessor(sym, as_of_date),
            reason=record.reason,
            confidence=record.confidence,
            notes=record.notes.copy(),
            metadata=record.metadata.copy()
        )

    def resolve_many(self, symbols: List[str], as_of_date: Optional[str] = None) -> List[SymbolLifecycleRecord]:
        return [self.resolve_status(s, as_of_date) for s in symbols]

    def resolve_successor(self, symbol: str, as_of_date: Optional[str] = None) -> Optional[str]:
        alias = alias_for_old_symbol(self.aliases, symbol)
        if alias:
            if as_of_date and alias.effective_date and alias.effective_date > as_of_date:
                return None
            return alias.new_symbol
        return None

    def resolve_predecessor(self, symbol: str, as_of_date: Optional[str] = None) -> Optional[str]:
        sym = symbol.upper()
        for a in self.aliases:
            if a.new_symbol == sym:
                if as_of_date and a.effective_date and a.effective_date > as_of_date:
                    continue
                return a.old_symbol
        return None

    def is_active(self, symbol: str, as_of_date: Optional[str] = None) -> bool:
        record = self.resolve_status(symbol, as_of_date)
        return record.status == SymbolLifecycleStatus.ACTIVE

    def requires_review(self, symbol: str, as_of_date: Optional[str] = None) -> bool:
        record = self.resolve_status(symbol, as_of_date)
        return record.status in [SymbolLifecycleStatus.UNKNOWN, SymbolLifecycleStatus.REVIEW_REQUIRED]
