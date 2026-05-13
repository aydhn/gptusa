"""Calendar reporting logic."""
from typing import Any
from usa_signal_bot.calendar.calendar_models import (
    MarketSession,
    TradingDayResult,
    SessionValidationResult,
    CalendarReviewResult
)

def market_session_to_text(session: MarketSession) -> str:
    parts = [
        f"Session: {session.date}",
        f"  Type: {session.session_type.value if hasattr(session.session_type, 'value') else str(session.session_type)}",
        f"  Trading: {session.is_trading_session}",
        f"  Early Close: {session.is_early_close}"
    ]
    if session.open_time_local and session.close_time_local:
        parts.append(f"  Times: {session.open_time_local} - {session.close_time_local} {session.timezone}")
    return "\n".join(parts)

def trading_day_result_to_text(result: TradingDayResult) -> str:
    parts = [
        f"Date: {result.date}",
        f"  Type: {result.day_type.value if hasattr(result.day_type, 'value') else str(result.day_type)}",
        f"  Is Trading Day: {result.is_trading_day}"
    ]
    if result.previous_trading_day:
        parts.append(f"  Prev: {result.previous_trading_day}")
    if result.next_trading_day:
        parts.append(f"  Next: {result.next_trading_day}")
    return "\n".join(parts)

def session_validation_result_to_text(result: SessionValidationResult) -> str:
    from usa_signal_bot.calendar.session_validation import session_validation_summary_to_text
    return session_validation_summary_to_text(result)

def calendar_review_result_to_text(result: CalendarReviewResult, limit: int = 50) -> str:
    lines = [
        f"=== Calendar Review: {result.review_id} ===",
        f"Report Type: {result.report_type.value if hasattr(result.report_type, 'value') else str(result.report_type)}",
        f"Calendar: {result.calendar_name.value if hasattr(result.calendar_name, 'value') else str(result.calendar_name)}",
        f"Created: {result.created_at_utc}",
        f"Total Trading Days Checked: {len(result.trading_day_results)}",
        f"Total Validations: {len(result.session_validations)}"
    ]
    if result.errors:
        lines.append("Errors:")
        for err in result.errors:
            lines.append(f"  - {err}")

    if result.session_validations:
        lines.append("\nSession Validation Highlights:")
        for v in result.session_validations[:limit]:
            lines.append(f"  {v.symbol}: {v.status.value if hasattr(v.status, 'value') else str(v.status)} (Missing: {v.missing_trading_days}, Non-trading: {v.non_trading_day_rows})")
        if len(result.session_validations) > limit:
            lines.append(f"  ... and {len(result.session_validations) - limit} more.")

    lines.append("\n" + calendar_limitations_text())
    return "\n".join(lines)

def calendar_store_summary_to_text(summary: dict[str, Any]) -> str:
    lines = [
        "=== Calendar Store Summary ===",
        f"Reviews count: {summary.get('reviews_count', 0)}",
        f"Latest review: {summary.get('latest_review', 'None')}",
        f"Validations count: {summary.get('validations_count', 0)}",
        f"Session files count: {summary.get('sessions_files_count', 0)}"
    ]
    return "\n".join(lines)

def calendar_limitations_text() -> str:
    return (
        "CALENDAR LIMITATIONS & DISCLAIMERS:\n"
        "- This is a strictly local/manual calendar implementation.\n"
        "- It DOES NOT guarantee exact official exchange calendar dates or early closes.\n"
        "- Output from this calendar module is for local operational guardrails only.\n"
        "- It DOES NOT constitute investment advice.\n"
        "- A VALID session status is NOT a live trading approval."
    )
