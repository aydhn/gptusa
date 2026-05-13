"""Manual holiday/early-close store."""
import json
from pathlib import Path
from typing import Any

from usa_signal_bot.core.enums import MarketCalendarName, CalendarDataSource
from usa_signal_bot.core.exceptions import HolidayStoreError
from usa_signal_bot.calendar.calendar_models import MarketHoliday, MarketEarlyClose

def default_us_equities_holidays() -> list[MarketHoliday]:
    # Limited placeholder for tests/examples
    return [
        MarketHoliday("2024-01-01", "New Year's Day", MarketCalendarName.US_EQUITIES, CalendarDataSource.STATIC_DEFAULT),
        MarketHoliday("2024-01-15", "Martin Luther King Jr. Day", MarketCalendarName.US_EQUITIES, CalendarDataSource.STATIC_DEFAULT),
        MarketHoliday("2024-02-19", "Washington's Birthday", MarketCalendarName.US_EQUITIES, CalendarDataSource.STATIC_DEFAULT),
        MarketHoliday("2024-03-29", "Good Friday", MarketCalendarName.US_EQUITIES, CalendarDataSource.STATIC_DEFAULT),
        MarketHoliday("2024-05-27", "Memorial Day", MarketCalendarName.US_EQUITIES, CalendarDataSource.STATIC_DEFAULT),
        MarketHoliday("2024-06-19", "Juneteenth National Independence Day", MarketCalendarName.US_EQUITIES, CalendarDataSource.STATIC_DEFAULT),
        MarketHoliday("2024-07-04", "Independence Day", MarketCalendarName.US_EQUITIES, CalendarDataSource.STATIC_DEFAULT),
        MarketHoliday("2024-09-02", "Labor Day", MarketCalendarName.US_EQUITIES, CalendarDataSource.STATIC_DEFAULT),
        MarketHoliday("2024-11-28", "Thanksgiving Day", MarketCalendarName.US_EQUITIES, CalendarDataSource.STATIC_DEFAULT),
        MarketHoliday("2024-12-25", "Christmas Day", MarketCalendarName.US_EQUITIES, CalendarDataSource.STATIC_DEFAULT),
    ]

def default_us_equities_early_closes() -> list[MarketEarlyClose]:
    return [
        MarketEarlyClose("2024-07-03", "13:00", "Day before Independence Day", MarketCalendarName.US_EQUITIES, CalendarDataSource.STATIC_DEFAULT),
        MarketEarlyClose("2024-11-29", "13:00", "Day after Thanksgiving", MarketCalendarName.US_EQUITIES, CalendarDataSource.STATIC_DEFAULT),
        MarketEarlyClose("2024-12-24", "13:00", "Christmas Eve", MarketCalendarName.US_EQUITIES, CalendarDataSource.STATIC_DEFAULT),
    ]

def load_holidays_from_json(path: Path) -> list[MarketHoliday]:
    if not path.is_file():
        raise HolidayStoreError(f"Holiday file not found: {path}")
    if ".." in str(path):
        raise HolidayStoreError("Path traversal prevented.")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        holidays = []
        for item in data:
            holidays.append(MarketHoliday(
                date=item["date"],
                name=item["name"],
                calendar_name=MarketCalendarName(item.get("calendar_name", "US_EQUITIES")),
                source=CalendarDataSource.MANUAL_FILE,
                metadata=item.get("metadata", {})
            ))
        return holidays
    except Exception as e:
        raise HolidayStoreError(f"Failed to load holidays from {path}: {e}")

def load_early_closes_from_json(path: Path) -> list[MarketEarlyClose]:
    if not path.is_file():
        raise HolidayStoreError(f"Early close file not found: {path}")
    if ".." in str(path):
        raise HolidayStoreError("Path traversal prevented.")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        closes = []
        for item in data:
            closes.append(MarketEarlyClose(
                date=item["date"],
                close_time_local=item["close_time_local"],
                name=item["name"],
                calendar_name=MarketCalendarName(item.get("calendar_name", "US_EQUITIES")),
                source=CalendarDataSource.MANUAL_FILE,
                metadata=item.get("metadata", {})
            ))
        return closes
    except Exception as e:
        raise HolidayStoreError(f"Failed to load early closes from {path}: {e}")

def write_example_holiday_file(path: Path) -> Path:
    if ".." in str(path):
        raise HolidayStoreError("Path traversal prevented.")
    path.parent.mkdir(parents=True, exist_ok=True)
    holidays = default_us_equities_holidays()
    data = []
    for h in holidays:
        data.append({
            "date": h.date,
            "name": h.name,
            "calendar_name": h.calendar_name.value
        })
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return path

def write_example_early_close_file(path: Path) -> Path:
    if ".." in str(path):
        raise HolidayStoreError("Path traversal prevented.")
    path.parent.mkdir(parents=True, exist_ok=True)
    closes = default_us_equities_early_closes()
    data = []
    for c in closes:
        data.append({
            "date": c.date,
            "close_time_local": c.close_time_local,
            "name": c.name,
            "calendar_name": c.calendar_name.value
        })
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return path

def merge_holidays(primary: list[MarketHoliday], manual: list[MarketHoliday]) -> list[MarketHoliday]:
    merged_dict = {h.date: h for h in primary}
    for m in manual:
        merged_dict[m.date] = m # manual overrides primary
    return sorted(list(merged_dict.values()), key=lambda x: x.date)

def merge_early_closes(primary: list[MarketEarlyClose], manual: list[MarketEarlyClose]) -> list[MarketEarlyClose]:
    merged_dict = {c.date: c for c in primary}
    for m in manual:
        merged_dict[m.date] = m # manual overrides primary
    return sorted(list(merged_dict.values()), key=lambda x: x.date)

def holidays_to_text(holidays: list[MarketHoliday]) -> str:
    lines = ["Market Holidays:"]
    for h in holidays:
        lines.append(f"  {h.date}: {h.name} ({h.source})")
    return "\n".join(lines)

def early_closes_to_text(items: list[MarketEarlyClose]) -> str:
    lines = ["Early Closes:"]
    for c in items:
        lines.append(f"  {c.date} @ {c.close_time_local}: {c.name} ({c.source})")
    return "\n".join(lines)
