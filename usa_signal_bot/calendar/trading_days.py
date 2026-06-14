"""Trading days helpers."""

from datetime import date, datetime, timedelta
from typing import Any
from usa_signal_bot.calendar.market_calendar import LocalMarketCalendar


def parse_date(date_str: str) -> date:
    if " " in date_str or "T" in date_str:
        # handle datetime string loosely
        date_str = date_str[:10]
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def format_date(d: date) -> str:
    return d.strftime("%Y-%m-%d")


def date_range(start_date: str, end_date: str) -> list[str]:
    start_dt = parse_date(start_date)
    end_dt = parse_date(end_date)

    days = []
    curr = start_dt
    while curr <= end_dt:
        days.append(format_date(curr))
        curr += timedelta(days=1)
    return days


def count_trading_days(
    calendar: LocalMarketCalendar, start_date: str, end_date: str
) -> int:
    return len(calendar.trading_days_between(start_date, end_date))


def align_rows_to_trading_days(
    rows: list[dict[str, Any]], calendar: LocalMarketCalendar
) -> dict[str, Any]:
    if not rows:
        return {"aligned_count": 0, "missing_count": 0, "extra_count": 0}

    # Assume rows are sorted by date
    actual_set = {
        d_val[:10]
        for r in rows
        if isinstance(d_val := (r.get("date") or r.get("timestamp") or ""), str)
        and len(d_val) >= 10
    }

    if not actual_set:
        return {"aligned_count": 0, "missing_count": 0, "extra_count": 0}

    start_date = min(actual_set)
    end_date = max(actual_set)

    expected_days = calendar.trading_days_between(start_date, end_date)
    expected_set = set(expected_days)

    missing = expected_set - actual_set
    extra = actual_set - expected_set

    return {
        "aligned_count": len(actual_set.intersection(expected_set)),
        "missing_count": len(missing),
        "extra_count": len(extra),
        "missing_days": sorted(list(missing)),
        "extra_days": sorted(list(extra)),
    }


def missing_trading_days_for_rows(
    rows: list[dict[str, Any]],
    calendar: LocalMarketCalendar,
    start_date: str | None = None,
    end_date: str | None = None,
) -> list[str]:
    actual_set = {
        d_val[:10]
        for r in rows
        if isinstance(d_val := (r.get("date") or r.get("timestamp") or ""), str)
        and len(d_val) >= 10
    }

    if not actual_set and not start_date and not end_date:
        return []

    start = start_date or (min(actual_set) if actual_set else "")
    end = end_date or (max(actual_set) if actual_set else "")

    if not start or not end:
        return []

    expected_days = calendar.trading_days_between(start, end)
    expected_set = set(expected_days)

    return sorted(list(expected_set - actual_set))


def non_trading_day_rows(
    rows: list[dict[str, Any]], calendar: LocalMarketCalendar
) -> list[dict[str, Any]]:
    return [
        r
        for r in rows
        if isinstance(d_val := (r.get("date") or r.get("timestamp") or ""), str)
        and len(d_val) >= 10
        and not calendar.is_trading_day(d_val[:10])
    ]


def trading_days_to_text(days: list[str]) -> str:
    if not days:
        return "No trading days."
    return f"Trading days ({len(days)}): " + ", ".join(days)
