"""Bar/Session alignment validation."""
from typing import Any
from datetime import datetime, timezone

from usa_signal_bot.core.enums import SessionValidationStatus
from usa_signal_bot.calendar.calendar_models import SessionValidationResult, create_session_validation_id
from usa_signal_bot.calendar.market_calendar import LocalMarketCalendar
from usa_signal_bot.calendar.trading_days import missing_trading_days_for_rows, non_trading_day_rows, count_trading_days

def validate_rows_against_calendar(symbol: str, rows: list[dict[str, Any]], calendar: LocalMarketCalendar) -> SessionValidationResult:
    created_at = datetime.now(timezone.utc).isoformat()
    validation_id = create_session_validation_id(symbol)

    if not rows:
        return SessionValidationResult(
            validation_id=validation_id,
            created_at_utc=created_at,
            symbol=symbol,
            calendar_name=calendar.calendar_name,
            status=SessionValidationStatus.MISSING,
            row_count=0,
            trading_day_count=0,
            non_trading_day_rows=0,
            missing_trading_days=0,
            early_close_rows=0,
            warnings=["No rows provided for validation."],
            errors=[]
        )

    dates = []
    early_close_count = 0
    for r in rows:
        d_val = r.get("date") or r.get("timestamp") or ""
        if isinstance(d_val, str) and len(d_val) >= 10:
            date_str = d_val[:10]
            dates.append(date_str)
            if calendar.is_early_close(date_str):
                early_close_count += 1

    start_date = min(dates) if dates else ""
    end_date = max(dates) if dates else ""

    trading_day_cnt = count_trading_days(calendar, start_date, end_date) if start_date else 0
    missing_days = missing_trading_days_for_rows(rows, calendar, start_date, end_date)
    non_trading_rows = non_trading_day_rows(rows, calendar)

    warnings = []
    errors = []

    status = SessionValidationStatus.VALID

    if missing_days:
        warnings.append(f"Missing {len(missing_days)} trading days.")
        status = SessionValidationStatus.WARNING

    if non_trading_rows:
        errors.append(f"Found {len(non_trading_rows)} rows on non-trading days.")
        status = SessionValidationStatus.INVALID

    if early_close_count > 0:
        warnings.append(f"Found {early_close_count} early close days.")

    if len(missing_days) > 10 and len(missing_days) > len(rows) * 0.1:
        errors.append("Too many missing trading days.")
        status = SessionValidationStatus.INVALID

    return SessionValidationResult(
        validation_id=validation_id,
        created_at_utc=created_at,
        symbol=symbol,
        calendar_name=calendar.calendar_name,
        status=status,
        row_count=len(rows),
        trading_day_count=trading_day_cnt,
        non_trading_day_rows=len(non_trading_rows),
        missing_trading_days=len(missing_days),
        early_close_rows=early_close_count,
        warnings=warnings,
        errors=errors,
        metadata={"missing_days": missing_days[:10], "non_trading_dates": [r.get("date", "")[:10] for r in non_trading_rows[:10]]}
    )



def validate_missing_sessions(symbol: str, rows: list[dict[str, Any]], calendar: LocalMarketCalendar) -> tuple[list[str], list[str]]:
    missing = missing_trading_days_for_rows(rows, calendar)
    warnings = []
    errors = []
    if missing:
        warnings.append(f"Symbol {symbol} is missing {len(missing)} trading sessions.")
    return missing, warnings

def validate_non_trading_rows(symbol: str, rows: list[dict[str, Any]], calendar: LocalMarketCalendar) -> tuple[list[dict[str, Any]], list[str]]:
    non_trading = non_trading_day_rows(rows, calendar)
    errors = []
    if non_trading:
        errors.append(f"Symbol {symbol} has {len(non_trading)} rows on non-trading days.")
    return non_trading, errors

def session_validation_summary_to_text(result: SessionValidationResult) -> str:
    lines = [
        f"Session Validation for {result.symbol}: {result.status.value if hasattr(result.status, 'value') else str(result.status)}",
        f"  Total Rows: {result.row_count}",
        f"  Expected Trading Days: {result.trading_day_count}",
        f"  Missing Days: {result.missing_trading_days}",
        f"  Non-trading Rows: {result.non_trading_day_rows}",
        f"  Early Close Rows: {result.early_close_rows}"
    ]
    if result.warnings:
        lines.append("  Warnings:")
        for w in result.warnings:
            lines.append(f"    - {w}")
    if result.errors:
        lines.append("  Errors:")
        for e in result.errors:
            lines.append(f"    - {e}")
    return "\n".join(lines)
