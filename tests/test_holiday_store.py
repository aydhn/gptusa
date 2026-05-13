"""Test holiday store."""
from pathlib import Path
from usa_signal_bot.calendar.holiday_store import default_us_equities_holidays, default_us_equities_early_closes, write_example_holiday_file, load_holidays_from_json, merge_holidays, holidays_to_text

def test_holiday_store_defaults():
    assert len(default_us_equities_holidays()) > 0
    assert len(default_us_equities_early_closes()) > 0

def test_holiday_store_write_read(tmp_path):
    p = tmp_path / "holidays.json"
    write_example_holiday_file(p)
    loaded = load_holidays_from_json(p)
    assert len(loaded) == len(default_us_equities_holidays())

def test_holiday_store_merge():
    h1 = default_us_equities_holidays()[:2]
    # Override
    h1[0].name = "Updated"
    merged = merge_holidays(default_us_equities_holidays(), h1)
    assert any(h.name == "Updated" for h in merged)

def test_holiday_store_text():
    h = default_us_equities_holidays()
    txt = holidays_to_text(h)
    assert "Market Holidays:" in txt
