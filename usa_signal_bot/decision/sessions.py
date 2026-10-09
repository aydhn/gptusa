"""NYSE regular-session calendar (America/New_York, DST-aware): holidays, early closes, session bounds.

Rule based, no external data. Covers the standard full-day holidays and 13:00 early closes.
"""

from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import Dict, Optional, Tuple
from zoneinfo import ZoneInfo

import pandas as pd

NY = ZoneInfo("America/New_York")
OPEN_TIME = time(9, 30)
CLOSE_TIME = time(16, 0)
EARLY_CLOSE_TIME = time(13, 0)


def easter(year: int) -> date:
    """Gregorian Easter Sunday (anonymous algorithm)."""
    a, b, c = year % 19, year // 100, year % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = (h + l - 7 * m + 114) % 31 + 1
    return date(year, month, day)


def _nth_weekday(year: int, month: int, weekday: int, n: int) -> date:
    d = date(year, month, 1)
    d += timedelta(days=(weekday - d.weekday()) % 7)
    return d + timedelta(weeks=n - 1)


def _last_weekday(year: int, month: int, weekday: int) -> date:
    d = date(year + (month == 12), month % 12 + 1, 1) - timedelta(days=1)
    return d - timedelta(days=(d.weekday() - weekday) % 7)


def _observed(d: date, allow_prev_year: bool = True) -> Optional[date]:
    if d.weekday() == 5:  # Saturday -> Friday
        return d - timedelta(days=1) if allow_prev_year else None
    if d.weekday() == 6:  # Sunday -> Monday
        return d + timedelta(days=1)
    return d


def nyse_holidays(year: int) -> Dict[date, str]:
    out: Dict[date, str] = {}

    def add(d: Optional[date], name: str) -> None:
        if d is not None and d.year == year:
            out[d] = name

    add(_observed(date(year, 1, 1), allow_prev_year=False), "New Year's Day")
    add(_nth_weekday(year, 1, 0, 3), "Martin Luther King Jr. Day")
    add(_nth_weekday(year, 2, 0, 3), "Washington's Birthday")
    add(easter(year) - timedelta(days=2), "Good Friday")
    add(_last_weekday(year, 5, 0), "Memorial Day")
    if year >= 2022:
        add(_observed(date(year, 6, 19)), "Juneteenth")
    add(_observed(date(year, 7, 4)), "Independence Day")
    add(_nth_weekday(year, 9, 0, 1), "Labor Day")
    add(_nth_weekday(year, 11, 3, 4), "Thanksgiving Day")
    add(_observed(date(year, 12, 25)), "Christmas Day")
    return out


def early_close_days(year: int) -> Dict[date, str]:
    out: Dict[date, str] = {}
    hol = nyse_holidays(year)
    jul3 = date(year, 7, 3)
    if jul3.weekday() < 4 and jul3 not in hol and date(year, 7, 4).weekday() < 5:
        out[jul3] = "Day before Independence Day"
    out[_nth_weekday(year, 11, 3, 4) + timedelta(days=1)] = "Day after Thanksgiving"
    dec24 = date(year, 12, 24)
    if dec24.weekday() < 4 and dec24 not in hol:
        out[dec24] = "Christmas Eve"
    return out


def is_trading_day(d: date) -> bool:
    return d.weekday() < 5 and d not in nyse_holidays(d.year)


def session_bounds(d: date) -> Optional[Tuple[datetime, datetime]]:
    """(open, close) as tz-aware America/New_York datetimes, or None if the market is closed."""
    if not is_trading_day(d):
        return None
    close_t = EARLY_CLOSE_TIME if d in early_close_days(d.year) else CLOSE_TIME
    return (datetime.combine(d, OPEN_TIME, tzinfo=NY), datetime.combine(d, close_t, tzinfo=NY))


def is_regular_session(ts: datetime) -> bool:
    """True for timestamps inside [open, close) of a trading day. Naive timestamps are rejected."""
    if ts.tzinfo is None:
        raise ValueError("timestamp must be timezone-aware (UTC or America/New_York)")
    local = ts.astimezone(NY)
    bounds = session_bounds(local.date())
    return bounds is not None and bounds[0] <= local < bounds[1]


def regular_session_mask(index: pd.DatetimeIndex) -> pd.Series:
    """Boolean mask for a tz-aware intraday index; use it to drop pre/post-market and holiday bars."""
    if index.tz is None:
        raise ValueError("intraday index must be timezone-aware")
    local = index.tz_convert(NY)
    flags = [is_regular_session(ts.to_pydatetime()) for ts in local]
    return pd.Series(flags, index=index)
