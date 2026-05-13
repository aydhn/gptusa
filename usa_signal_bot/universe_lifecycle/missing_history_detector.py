from typing import Any, List, Optional, Tuple, Dict
import datetime
from usa_signal_bot.core.enums import SymbolHistoryStatus
from usa_signal_bot.universe_lifecycle.lifecycle_models import SymbolHistoryCheck, create_symbol_history_check_id
from usa_signal_bot.providers.provider_models import ProviderResponse

def history_rows_first_last_dates(rows: List[Dict[str, Any]]) -> Tuple[Optional[str], Optional[str]]:
    if not rows:
        return None, None
    dates = []
    for r in rows:
        d = r.get("timestamp_utc") or r.get("date") or r.get("Date")
        if d:
            dates.append(str(d)[:10])
    if not dates:
        return None, None
    dates.sort()
    return dates[0], dates[-1]

def estimate_missing_rows_from_calendar(rows: List[Dict[str, Any]], calendar: Optional[Any] = None) -> Optional[int]:
    if not rows:
        return None
    return None

def check_symbol_history(
    symbol: str,
    rows: List[Dict[str, Any]],
    min_rows: int = 120,
    min_history_days: Optional[int] = 180,
    max_stale_days: int = 14
) -> SymbolHistoryCheck:
    first_date, last_date = history_rows_first_last_dates(rows)
    row_count = len(rows)
    status = SymbolHistoryStatus.SUFFICIENT
    stale_days = None
    warnings = []

    if row_count == 0:
        status = SymbolHistoryStatus.MISSING_HISTORY
        warnings.append("No historical data found.")
    else:
        now = datetime.datetime.now(datetime.timezone.utc)
        if last_date:
            try:
                last_dt = datetime.datetime.fromisoformat(last_date.replace("Z", "+00:00"))
                if last_dt.tzinfo is None:
                    last_dt = last_dt.replace(tzinfo=datetime.timezone.utc)
                stale_days = (now - last_dt).days
                if stale_days > max_stale_days:
                    status = SymbolHistoryStatus.STALE_HISTORY
                    warnings.append(f"Data is stale by {stale_days} days (max allowed: {max_stale_days}).")
            except ValueError:
                pass
        if status != SymbolHistoryStatus.STALE_HISTORY:
            if row_count < min_rows:
                status = SymbolHistoryStatus.SHORT_HISTORY
                warnings.append(f"Short history: {row_count} rows < {min_rows} minimum.")
            elif first_date and last_date and min_history_days:
                try:
                    f_dt = datetime.datetime.fromisoformat(first_date.replace("Z", "+00:00"))
                    l_dt = datetime.datetime.fromisoformat(last_date.replace("Z", "+00:00"))
                    diff = (l_dt - f_dt).days
                    if diff < min_history_days:
                        status = SymbolHistoryStatus.SHORT_HISTORY
                        warnings.append(f"History spans {diff} days, requiring {min_history_days}.")
                except ValueError:
                    pass

    return SymbolHistoryCheck(
        check_id=create_symbol_history_check_id(symbol),
        symbol=symbol.upper(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        status=status,
        row_count=row_count,
        first_date=first_date,
        last_date=last_date,
        stale_days=stale_days,
        warnings=warnings,
        errors=[]
    )

def check_provider_response_history(response: ProviderResponse, min_rows: int = 120) -> List[SymbolHistoryCheck]:
    checks = []
    if not response.ohlcv_data:
        return checks
    for sym, rows in response.ohlcv_data.items():
        dict_rows = [r.to_dict() if hasattr(r, 'to_dict') else r.__dict__ for r in rows]
        checks.append(check_symbol_history(sym, dict_rows, min_rows=min_rows))
    return checks

def symbol_history_check_to_text(check: SymbolHistoryCheck) -> str:
    lines = [
        f"History Check: {check.symbol} [{check.status.value}]",
        f"Rows: {check.row_count} | First: {check.first_date} | Last: {check.last_date}"
    ]
    if check.stale_days is not None:
        lines.append(f"Stale Days: {check.stale_days}")
    if check.warnings:
        for w in check.warnings:
            lines.append(f"  Warning: {w}")
    return "\n".join(lines)
