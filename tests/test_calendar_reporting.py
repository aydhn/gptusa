"""Test calendar reporting."""
from usa_signal_bot.calendar.calendar_reporting import calendar_limitations_text

def test_calendar_reporting():
    txt = calendar_limitations_text()
    assert "NOT an official exchange calendar" in txt or "DOES NOT guarantee exact official exchange calendar dates" in txt
