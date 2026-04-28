import pytest
from usa_signal_bot.storage.csv_store import write_csv, read_csv, infer_fieldnames
from usa_signal_bot.core.exceptions import ValidationError

def test_csv_write_read(tmp_path):
    file_path = tmp_path / "test.csv"
    rows = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]

    write_csv(file_path, rows)
    assert file_path.exists()

    loaded = read_csv(file_path)
    assert len(loaded) == 2
    assert loaded[0]["id"] == "1"
    assert loaded[0]["name"] == "Alice"

def test_csv_infer_fieldnames():
    rows = [{"a": 1, "b": 2}, {"b": 3, "c": 4}]
    fields = infer_fieldnames(rows)
    assert sorted(fields) == ["a", "b", "c"]

def test_csv_empty_rows(tmp_path):
    file_path = tmp_path / "empty.csv"
    with pytest.raises(ValidationError):
        write_csv(file_path, [])

    # Should work if fieldnames are provided
    write_csv(file_path, [], fieldnames=["id"])
    assert file_path.exists()
    assert len(read_csv(file_path)) == 0
