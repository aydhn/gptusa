"""Test holiday store."""

from pathlib import Path
from usa_signal_bot.calendar.holiday_store import (
    default_us_equities_holidays,
    default_us_equities_early_closes,
    write_example_holiday_file,
    load_holidays_from_json,
    merge_holidays,
    holidays_to_text,
    write_example_early_close_file,
    load_early_closes_from_json,
)
import pytest
from usa_signal_bot.core.exceptions import HolidayStoreError


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


def test_early_closes_store_write_read(tmp_path):
    p = tmp_path / "early_closes.json"
    write_example_early_close_file(p)
    loaded = load_early_closes_from_json(p)
    assert len(loaded) == len(default_us_equities_early_closes())


def test_early_closes_missing_file(tmp_path):
    p = tmp_path / "nonexistent_early_closes.json"
    with pytest.raises(HolidayStoreError, match="Early close file not found"):
        load_early_closes_from_json(p)


def test_early_closes_path_traversal():
    p = Path("../early_closes.json")
    with pytest.raises(HolidayStoreError):
        load_early_closes_from_json(p)


def test_write_example_early_close_file_path_traversal():
    p = Path("../write_early_closes.json")
    with pytest.raises(HolidayStoreError, match="Path traversal prevented."):
        write_example_early_close_file(p)


def test_write_example_early_close_file_success(tmp_path):
    import json

    p = tmp_path / "new_early_closes.json"
    result_path = write_example_early_close_file(p)
    assert result_path == p
    assert p.is_file()
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == len(default_us_equities_early_closes())
