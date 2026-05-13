from typing import Any, List, Dict
from usa_signal_bot.core.enums import SymbolHistoryStatus, SymbolLifecycleStatus
from usa_signal_bot.universe_lifecycle.lifecycle_models import SymbolHistoryCheck, SymbolLifecycleRecord

def detect_stale_symbols(history_checks: List[SymbolHistoryCheck], max_stale_days: int = 14) -> List[SymbolHistoryCheck]:
    return [c for c in history_checks if c.status == SymbolHistoryStatus.STALE_HISTORY or (c.stale_days is not None and c.stale_days > max_stale_days)]

def detect_symbols_with_missing_history(history_checks: List[SymbolHistoryCheck]) -> List[SymbolHistoryCheck]:
    return [c for c in history_checks if c.status == SymbolHistoryStatus.MISSING_HISTORY]

def detect_symbols_requiring_review(records: List[SymbolLifecycleRecord], history_checks: List[SymbolHistoryCheck]) -> List[str]:
    stale_map = {c.symbol: c for c in history_checks if c.status in [SymbolHistoryStatus.STALE_HISTORY, SymbolHistoryStatus.MISSING_HISTORY]}
    review_list = []
    for r in records:
        if r.status in [SymbolLifecycleStatus.UNKNOWN, SymbolLifecycleStatus.REVIEW_REQUIRED]:
            review_list.append(r.symbol)
        elif r.status == SymbolLifecycleStatus.ACTIVE and r.symbol in stale_map:
            review_list.append(r.symbol)
    return sorted(list(set(review_list)))

def stale_symbol_summary(history_checks: List[SymbolHistoryCheck]) -> Dict[str, Any]:
    stale = detect_stale_symbols(history_checks)
    missing = detect_symbols_with_missing_history(history_checks)
    short = [c for c in history_checks if c.status == SymbolHistoryStatus.SHORT_HISTORY]
    sufficient = [c for c in history_checks if c.status == SymbolHistoryStatus.SUFFICIENT]
    return {
        "total_checks": len(history_checks),
        "sufficient_count": len(sufficient),
        "stale_count": len(stale),
        "missing_count": len(missing),
        "short_count": len(short),
        "stale_symbols": [c.symbol for c in stale],
        "missing_symbols": [c.symbol for c in missing]
    }

def stale_symbol_summary_to_text(summary: Dict[str, Any]) -> str:
    lines = [
        "Stale Symbol Summary:",
        f"Total Checked: {summary['total_checks']}",
        f"Sufficient: {summary['sufficient_count']}",
        f"Stale: {summary['stale_count']}",
        f"Missing: {summary['missing_count']}",
        f"Short: {summary['short_count']}"
    ]
    if summary['stale_symbols']:
        lines.append(f"Stale Symbols: {', '.join(summary['stale_symbols'][:20])}" + ("..." if summary['stale_count'] > 20 else ""))
    if summary['missing_symbols']:
        lines.append(f"Missing Symbols: {', '.join(summary['missing_symbols'][:20])}" + ("..." if summary['missing_count'] > 20 else ""))
    return "\n".join(lines)
