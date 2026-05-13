"""Session classification."""
from typing import Any
from usa_signal_bot.core.enums import MarketSessionType
from usa_signal_bot.calendar.market_calendar import LocalMarketCalendar

def classify_timestamp_session(timestamp_str: str, calendar: LocalMarketCalendar) -> MarketSessionType:
    if not timestamp_str or len(timestamp_str) < 10:
        return MarketSessionType.UNKNOWN

    date_str = timestamp_str[:10]
    if calendar.is_weekend(date_str):
        return MarketSessionType.WEEKEND
    if calendar.is_holiday(date_str):
        return MarketSessionType.HOLIDAY

    # If no time component, assume regular trading day for daily bars
    if len(timestamp_str) <= 10 or " " not in timestamp_str and "T" not in timestamp_str:
        return MarketSessionType.REGULAR

    # Time component exists (intraday)
    time_part = timestamp_str[11:16] # extract HH:MM assuming YYYY-MM-DDTHH:MM... or YYYY-MM-DD HH:MM...
    if len(time_part) < 5:
        return MarketSessionType.REGULAR # fallback

    open_time, close_time = calendar.regular_session_times(date_str)

    if time_part < open_time:
        return MarketSessionType.PREMARKET
    elif time_part >= close_time:
        return MarketSessionType.AFTER_HOURS
    else:
        return MarketSessionType.REGULAR

def classify_bar_session(row: dict[str, Any], calendar: LocalMarketCalendar) -> MarketSessionType:
    timestamp = row.get("timestamp") or row.get("date") or ""
    return classify_timestamp_session(str(timestamp), calendar)

def classify_rows_by_session(rows: list[dict[str, Any]], calendar: LocalMarketCalendar) -> dict[str, int]:
    summary = {
        MarketSessionType.REGULAR.value: 0,
        MarketSessionType.PREMARKET.value: 0,
        MarketSessionType.AFTER_HOURS.value: 0,
        MarketSessionType.CLOSED.value: 0,
        MarketSessionType.HOLIDAY.value: 0,
        MarketSessionType.EARLY_CLOSE.value: 0,
        MarketSessionType.WEEKEND.value: 0,
        MarketSessionType.UNKNOWN.value: 0
    }

    for r in rows:
        session = classify_bar_session(r, calendar)
        # Handle early close flag specifically
        timestamp = str(r.get("timestamp") or r.get("date") or "")
        if timestamp and len(timestamp) >= 10:
            date_str = timestamp[:10]
            if session == MarketSessionType.REGULAR and calendar.is_early_close(date_str):
                summary[MarketSessionType.EARLY_CLOSE.value] += 1
            else:
                summary[session.value if hasattr(session, "value") else str(session)] += 1
        else:
            summary[session.value if hasattr(session, "value") else str(session)] += 1

    return summary

def session_type_to_signal_guard(session_type: MarketSessionType) -> dict[str, Any]:
    guard = {
        "is_trading_allowed": False,
        "warning": None,
        "metadata_flag": str(session_type)
    }

    if session_type == MarketSessionType.REGULAR:
        guard["is_trading_allowed"] = True
    elif session_type == MarketSessionType.EARLY_CLOSE:
        guard["is_trading_allowed"] = True
        guard["warning"] = "Session is early close."
    elif session_type == MarketSessionType.PREMARKET:
        guard["warning"] = "Premarket session. Proceed with caution."
    elif session_type == MarketSessionType.AFTER_HOURS:
        guard["warning"] = "After-hours session. Proceed with caution."
    elif session_type == MarketSessionType.WEEKEND:
        guard["warning"] = "Weekend. Market closed."
    elif session_type == MarketSessionType.HOLIDAY:
        guard["warning"] = "Holiday. Market closed."
    elif session_type == MarketSessionType.CLOSED:
        guard["warning"] = "Market closed."
    else:
        guard["warning"] = "Unknown session type."

    return guard

def session_summary_to_text(summary: dict[str, int]) -> str:
    lines = ["Session Summary:"]
    for k, v in summary.items():
        if v > 0:
            lines.append(f"  {k}: {v} rows")
    if len(lines) == 1:
        lines.append("  No data.")
    return "\n".join(lines)
