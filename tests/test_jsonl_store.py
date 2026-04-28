import pytest
from usa_signal_bot.storage.jsonl_store import append_jsonl, read_jsonl, tail_jsonl, count_jsonl, write_jsonl
from usa_signal_bot.core.exceptions import DataValidationError

def test_jsonl_operations(tmp_path):
    file_path = tmp_path / "test.jsonl"

    # Write and append
    append_jsonl(file_path, {"id": 1, "val": "A"})
    append_jsonl(file_path, {"id": 2, "val": "B"})

    assert count_jsonl(file_path) == 2

    # Read
    records = read_jsonl(file_path)
    assert len(records) == 2
    assert records[0]["id"] == 1
    assert records[1]["val"] == "B"

    # Tail
    append_jsonl(file_path, {"id": 3, "val": "C"})
    tail_records = tail_jsonl(file_path, 2)
    assert len(tail_records) == 2
    assert tail_records[0]["id"] == 2
    assert tail_records[1]["id"] == 3

def test_jsonl_write_list(tmp_path):
    file_path = tmp_path / "bulk.jsonl"
    records = [{"id": 1}, {"id": 2}, {"id": 3}]

    write_jsonl(file_path, records)
    assert count_jsonl(file_path) == 3

def test_jsonl_corrupt_line(tmp_path):
    file_path = tmp_path / "corrupt.jsonl"
    append_jsonl(file_path, {"id": 1})

    # Inject corrupt line
    with open(file_path, 'a') as f:
        f.write("{invalid json}\n")

    with pytest.raises(DataValidationError):
        read_jsonl(file_path)
