
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
import json

from usa_signal_bot.paper_readiness_board.board_store import (
    write_board_review_json,
    write_board_gates_jsonl,
    write_runtime_write_block_events_jsonl
)

@patch("usa_signal_bot.paper_readiness_board.board_store._ensure_dir")
@patch("builtins.open", new_callable=mock_open)
@patch("usa_signal_bot.paper_readiness_board.board_store.json.dump")
@patch("usa_signal_bot.paper_readiness_board.board_store.paper_readiness_board_review_to_dict")
def test_write_board_review_json(mock_to_dict, mock_json_dump, mock_file, mock_ensure_dir):
    path = Path("/tmp/fake_board_review.json")
    mock_item = MagicMock()
    mock_to_dict.return_value = {"fake": "data"}

    result = write_board_review_json(path, mock_item)

    mock_ensure_dir.assert_called_once_with(path.parent)
    mock_file.assert_called_once_with(path, "w")
    mock_json_dump.assert_called_once_with({"fake": "data"}, mock_file(), indent=2)
    assert result == path

@patch("usa_signal_bot.paper_readiness_board.board_store._ensure_dir")
@patch("builtins.open", new_callable=mock_open)
@patch("usa_signal_bot.paper_readiness_board.board_store.paper_readiness_board_gate_to_dict")
def test_write_board_gates_jsonl(mock_to_dict, mock_file, mock_ensure_dir):
    path = Path("/tmp/fake_board_gates.jsonl")
    mock_items = [MagicMock(), MagicMock()]
    mock_to_dict.side_effect = [{"fake": "data1"}, {"fake": "data2"}]

    result = write_board_gates_jsonl(path, mock_items)

    mock_ensure_dir.assert_called_once_with(path.parent)
    mock_file.assert_called_once_with(path, "w")

    # Check that write was called correctly with newline for jsonl
    handle = mock_file()
    assert handle.write.call_count == 2
    handle.write.assert_any_call('{"fake": "data1"}\n')
    handle.write.assert_any_call('{"fake": "data2"}\n')
    assert result == path

@patch("usa_signal_bot.paper_readiness_board.board_store._ensure_dir")
@patch("builtins.open", new_callable=mock_open)
@patch("usa_signal_bot.paper_readiness_board.board_store.runtime_write_block_event_to_dict")
def test_write_runtime_write_block_events_jsonl(mock_to_dict, mock_file, mock_ensure_dir):
    path = Path("/tmp/fake_write_block_events.jsonl")
    mock_items = [MagicMock()]
    mock_to_dict.return_value = {"fake": "event"}

    result = write_runtime_write_block_events_jsonl(path, mock_items)

    mock_ensure_dir.assert_called_once_with(path.parent)
    mock_file.assert_called_once_with(path, "w")

    # Check that write was called correctly
    handle = mock_file()
    handle.write.assert_called_once_with('{"fake": "event"}\n')
    assert result == path
