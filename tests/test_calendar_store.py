"""Test calendar store."""

import json
from unittest.mock import patch, MagicMock
from usa_signal_bot.calendar.calendar_store import (
    calendar_store_dir,
    write_calendar_review_result_json,
    list_calendar_reviews,
    write_session_validation_result_json,
    write_market_sessions_jsonl,
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


def test_write_market_sessions_jsonl_success(tmp_path):
    with patch(
        "usa_signal_bot.calendar.calendar_store.market_session_to_dict"
    ) as mock_to_dict:
        mock_to_dict.side_effect = [{"session_id": "sess_1"}, {"session_id": "sess_2"}]

        mock_s1 = MagicMock()
        mock_s2 = MagicMock()

        p = write_market_sessions_jsonl(
            tmp_path / "calendar" / "sessions" / "sessions.jsonl", [mock_s1, mock_s2]
        )

        assert p.exists()
        assert mock_to_dict.call_count == 2

        with open(p, "r", encoding="utf-8") as f:
            lines = f.readlines()

        assert len(lines) == 2
        assert json.loads(lines[0]) == {"session_id": "sess_1"}
        assert json.loads(lines[1]) == {"session_id": "sess_2"}


def test_write_market_sessions_jsonl_error(tmp_path):
    with patch("usa_signal_bot.calendar.calendar_store.open") as mock_open:
        mock_open.side_effect = PermissionError("Permission denied")

        mock_res = MagicMock()

        with pytest.raises(CalendarStorageError, match="Failed to write sessions to"):
            write_market_sessions_jsonl(
                tmp_path / "calendar" / "sessions" / "sessions.jsonl", [mock_res]
            )
