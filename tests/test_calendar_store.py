"""Test calendar store."""
from usa_signal_bot.calendar.calendar_store import calendar_store_dir, write_calendar_review_result_json, list_calendar_reviews
from usa_signal_bot.calendar.calendar_models import CalendarReviewResult
from usa_signal_bot.core.enums import CalendarReportType, MarketCalendarName

def test_calendar_store(tmp_path):
    res = CalendarReviewResult("id", "2024", CalendarReportType.CALENDAR_SUMMARY, MarketCalendarName.US_EQUITIES, [], [], [])
    p = write_calendar_review_result_json(tmp_path / "calendar" / "reviews" / "rev.json", res)
    assert p.exists()
    assert len(list_calendar_reviews(tmp_path)) == 1
