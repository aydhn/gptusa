"""Test calendar store."""

import json
from unittest.mock import patch, MagicMock
from usa_signal_bot.calendar.calendar_store import (
    calendar_store_dir,
    write_calendar_review_result_json,
    list_calendar_reviews,
    write_session_validation_result_json,
    read_calendar_review_result_json,
)
from usa_signal_bot.calendar.calendar_models import CalendarReviewResult
from usa_signal_bot.core.enums import CalendarReportType, MarketCalendarName
from usa_signal_bot.core.exceptions import CalendarStorageError
import pytest


def test_calendar_store(tmp_path):
    res = CalendarReviewResult(
        "id",
        "2024",
        CalendarReportType.CALENDAR_SUMMARY,
        MarketCalendarName.US_EQUITIES,
        [],
        [],
        [],
    )
    p = write_calendar_review_result_json(
        tmp_path / "calendar" / "reviews" / "rev.json", res
    )
    assert p.exists()
    assert len(list_calendar_reviews(tmp_path)) == 1


def test_write_session_validation_result_json_success(tmp_path):
    with patch(
        "usa_signal_bot.calendar.calendar_store.session_validation_result_to_dict"
    ) as mock_to_dict:
        mock_to_dict.return_value = {
            "validation_id": "val_1",
            "symbol": "AAPL",
            "metadata": {"key": "value"},
        }

        mock_res = MagicMock()

        p = write_session_validation_result_json(
            tmp_path / "calendar" / "session_validations" / "val_1.json", mock_res
        )

        assert p.exists()
        mock_to_dict.assert_called_once_with(mock_res)

        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["validation_id"] == "val_1"
        assert data["symbol"] == "AAPL"
        assert data["metadata"]["key"] == "value"


def test_write_session_validation_result_json_error(tmp_path):
    with patch("usa_signal_bot.calendar.calendar_store.open") as mock_open:
        mock_open.side_effect = PermissionError("Permission denied")

        mock_res = MagicMock()

        with pytest.raises(
            CalendarStorageError, match="Failed to write session validation"
        ):
            write_session_validation_result_json(
                tmp_path / "calendar" / "session_validations" / "val_1.json", mock_res
            )


def test_write_trading_day_results_jsonl_success(tmp_path):
    from usa_signal_bot.calendar.calendar_store import write_trading_day_results_jsonl

    with patch(
        "usa_signal_bot.calendar.calendar_store.trading_day_result_to_dict"
    ) as mock_to_dict:
        mock_to_dict.return_value = {
            "date": "2024-01-01",
            "is_trading_day": True,
            "holiday_name": None,
        }

        mock_res1 = MagicMock()
        mock_res2 = MagicMock()

        p = write_trading_day_results_jsonl(
            tmp_path / "calendar" / "trading_days.jsonl", [mock_res1, mock_res2]
        )

        assert p.exists()
        assert mock_to_dict.call_count == 2

        with open(p, "r", encoding="utf-8") as f:
            lines = f.readlines()

        assert len(lines) == 2
        data = json.loads(lines[0])
        assert data["date"] == "2024-01-01"
        assert data["is_trading_day"] is True


def test_write_trading_day_results_jsonl_error(tmp_path):
    from usa_signal_bot.calendar.calendar_store import write_trading_day_results_jsonl

    with patch("usa_signal_bot.calendar.calendar_store.open") as mock_open:
        mock_open.side_effect = PermissionError("Permission denied")

        mock_res = MagicMock()

        with pytest.raises(
            CalendarStorageError, match="Failed to write trading day results"
        ):
            write_trading_day_results_jsonl(
                tmp_path / "calendar" / "trading_days.jsonl", [mock_res]
            )


def test_read_calendar_review_result_json_success(tmp_path):
    import json

    path = tmp_path / "test_read.json"
    data = {"validation_id": "test_id", "symbol": "AAPL"}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    result = read_calendar_review_result_json(path)
    assert result == data


def test_read_calendar_review_result_json_not_found(tmp_path):
    path = tmp_path / "nonexistent.json"

    with pytest.raises(CalendarStorageError, match="Calendar review file not found"):
        read_calendar_review_result_json(path)


def test_read_calendar_review_result_json_error(tmp_path):
    path = tmp_path / "test_read_error.json"
    path.touch()  # Create the file so it exists

    with patch("usa_signal_bot.calendar.calendar_store.open") as mock_open:
        mock_open.side_effect = PermissionError("Permission denied")

        with pytest.raises(
            CalendarStorageError, match="Failed to read calendar review"
        ):
            read_calendar_review_result_json(path)
