"""Calendar and Session awareness models."""
from dataclasses import dataclass, field
from typing import Any
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    MarketCalendarName,
    MarketSessionType,
    MarketDayType,
    SessionValidationStatus,
    CalendarDataSource,
    CalendarReportType
)

@dataclass
class MarketHoliday:
    date: str
    name: str
    calendar_name: MarketCalendarName
    source: CalendarDataSource
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class MarketEarlyClose:
    date: str
    close_time_local: str
    name: str
    calendar_name: MarketCalendarName
    source: CalendarDataSource
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class MarketSession:
    session_id: str
    calendar_name: MarketCalendarName
    date: str
    session_type: MarketSessionType
    open_time_local: str | None
    close_time_local: str | None
    timezone: str
    is_trading_session: bool
    is_early_close: bool
    source: CalendarDataSource
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

@dataclass
class TradingDayResult:
    result_id: str
    calendar_name: MarketCalendarName
    date: str
    day_type: MarketDayType
    is_trading_day: bool
    previous_trading_day: str | None
    next_trading_day: str | None
    session: MarketSession | None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

@dataclass
class SessionValidationResult:
    validation_id: str
    created_at_utc: str
    symbol: str
    calendar_name: MarketCalendarName
    status: SessionValidationStatus
    row_count: int
    trading_day_count: int
    non_trading_day_rows: int
    missing_trading_days: int
    early_close_rows: int
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class CalendarReviewResult:
    review_id: str
    created_at_utc: str
    report_type: CalendarReportType
    calendar_name: MarketCalendarName
    sessions: list[MarketSession]
    trading_day_results: list[TradingDayResult]
    session_validations: list[SessionValidationResult]
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def market_holiday_to_dict(item: MarketHoliday) -> dict[str, Any]:
    return {
        "date": item.date,
        "name": item.name,
        "calendar_name": item.calendar_name.value if hasattr(item.calendar_name, "value") else str(item.calendar_name),
        "source": item.source.value if hasattr(item.source, "value") else str(item.source),
        "metadata": item.metadata
    }

def market_early_close_to_dict(item: MarketEarlyClose) -> dict[str, Any]:
    return {
        "date": item.date,
        "close_time_local": item.close_time_local,
        "name": item.name,
        "calendar_name": item.calendar_name.value if hasattr(item.calendar_name, "value") else str(item.calendar_name),
        "source": item.source.value if hasattr(item.source, "value") else str(item.source),
        "metadata": item.metadata
    }

def market_session_to_dict(session: MarketSession) -> dict[str, Any]:
    return {
        "session_id": session.session_id,
        "calendar_name": session.calendar_name.value if hasattr(session.calendar_name, "value") else str(session.calendar_name),
        "date": session.date,
        "session_type": session.session_type.value if hasattr(session.session_type, "value") else str(session.session_type),
        "open_time_local": session.open_time_local,
        "close_time_local": session.close_time_local,
        "timezone": session.timezone,
        "is_trading_session": session.is_trading_session,
        "is_early_close": session.is_early_close,
        "source": session.source.value if hasattr(session.source, "value") else str(session.source),
        "warnings": session.warnings,
        "errors": session.errors
    }

def trading_day_result_to_dict(result: TradingDayResult) -> dict[str, Any]:
    return {
        "result_id": result.result_id,
        "calendar_name": result.calendar_name.value if hasattr(result.calendar_name, "value") else str(result.calendar_name),
        "date": result.date,
        "day_type": result.day_type.value if hasattr(result.day_type, "value") else str(result.day_type),
        "is_trading_day": result.is_trading_day,
        "previous_trading_day": result.previous_trading_day,
        "next_trading_day": result.next_trading_day,
        "session": market_session_to_dict(result.session) if result.session else None,
        "warnings": result.warnings,
        "errors": result.errors
    }

def session_validation_result_to_dict(result: SessionValidationResult) -> dict[str, Any]:
    return {
        "validation_id": result.validation_id,
        "created_at_utc": result.created_at_utc,
        "symbol": result.symbol,
        "calendar_name": result.calendar_name.value if hasattr(result.calendar_name, "value") else str(result.calendar_name),
        "status": result.status.value if hasattr(result.status, "value") else str(result.status),
        "row_count": result.row_count,
        "trading_day_count": result.trading_day_count,
        "non_trading_day_rows": result.non_trading_day_rows,
        "missing_trading_days": result.missing_trading_days,
        "early_close_rows": result.early_close_rows,
        "warnings": result.warnings,
        "errors": result.errors,
        "metadata": result.metadata
    }

def calendar_review_result_to_dict(result: CalendarReviewResult) -> dict[str, Any]:
    return {
        "review_id": result.review_id,
        "created_at_utc": result.created_at_utc,
        "report_type": result.report_type.value if hasattr(result.report_type, "value") else str(result.report_type),
        "calendar_name": result.calendar_name.value if hasattr(result.calendar_name, "value") else str(result.calendar_name),
        "sessions": [market_session_to_dict(s) for s in result.sessions],
        "trading_day_results": [trading_day_result_to_dict(t) for t in result.trading_day_results],
        "session_validations": [session_validation_result_to_dict(v) for v in result.session_validations],
        "output_paths": result.output_paths,
        "warnings": result.warnings,
        "errors": result.errors
    }

def _validate_date_format(date_str: str) -> None:
    from usa_signal_bot.core.exceptions import MarketCalendarError
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise MarketCalendarError(f"Invalid date format, expected YYYY-MM-DD: {date_str}")

def _validate_time_format(time_str: str) -> None:
    from usa_signal_bot.core.exceptions import MarketCalendarError
    try:
        datetime.strptime(time_str, "%H:%M")
    except ValueError:
        raise MarketCalendarError(f"Invalid time format, expected HH:MM: {time_str}")

def validate_market_holiday(item: MarketHoliday) -> None:
    from usa_signal_bot.core.exceptions import MarketCalendarError
    _validate_date_format(item.date)

def validate_market_early_close(item: MarketEarlyClose) -> None:
    from usa_signal_bot.core.exceptions import MarketCalendarError
    _validate_date_format(item.date)
    _validate_time_format(item.close_time_local)

def validate_market_session(session: MarketSession) -> None:
    from usa_signal_bot.core.exceptions import MarketCalendarError
    _validate_date_format(session.date)
    if not session.timezone:
        raise MarketCalendarError("Timezone cannot be empty for MarketSession")
    if session.open_time_local:
        _validate_time_format(session.open_time_local)
    if session.close_time_local:
        _validate_time_format(session.close_time_local)
    if session.open_time_local and session.close_time_local:
        if session.open_time_local >= session.close_time_local:
            raise MarketCalendarError(f"Close time ({session.close_time_local}) must be after open time ({session.open_time_local})")

def validate_session_validation_result(result: SessionValidationResult) -> None:
    from usa_signal_bot.core.exceptions import MarketCalendarError
    pass # nothing to validate strictly here

def create_market_session_id(calendar_name: MarketCalendarName, date: str) -> str:
    cal_str = calendar_name.value if hasattr(calendar_name, "value") else str(calendar_name)
    return f"session_{cal_str}_{date}"

def create_trading_day_result_id(date: str) -> str:
    return f"trading_day_{date}"

def create_session_validation_id(symbol: str) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"session_val_{symbol}_{timestamp}"

def create_calendar_review_id(prefix: str = "calendar_review") -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{prefix}_{timestamp}"
