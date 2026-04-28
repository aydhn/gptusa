import pytest
from pathlib import Path
from dataclasses import dataclass
from usa_signal_bot.storage.json_store import write_json, read_json, write_model_json, read_json_dict
from usa_signal_bot.core.exceptions import StorageReadError

@dataclass
class DummyModel:
    name: str
    value: int

def test_json_write_read(tmp_path):
    file_path = tmp_path / "test.json"
    data = {"hello": "world", "items": [1, 2, 3]}

    write_json(file_path, data)
    assert file_path.exists()

    loaded = read_json(file_path)
    assert loaded == data

def test_write_model_json(tmp_path):
    file_path = tmp_path / "model.json"
    model = DummyModel(name="test", value=42)

    write_model_json(file_path, model)
    assert file_path.exists()

    loaded = read_json(file_path)
    assert loaded == {"name": "test", "value": 42}

def test_read_json_dict(tmp_path):
    file_path = tmp_path / "dict.json"
    write_json(file_path, {"a": 1})

    loaded = read_json_dict(file_path)
    assert loaded["a"] == 1

    # Test non-dict JSON
    list_path = tmp_path / "list.json"
    write_json(list_path, [1, 2, 3])

    with pytest.raises(StorageReadError):
        read_json_dict(list_path)

def test_atomic_write(tmp_path):
    file_path = tmp_path / "atomic.json"
    write_json(file_path, {"test": "data"}, atomic=True)
    assert file_path.exists()
    assert read_json(file_path) == {"test": "data"}

def test_invalid_path(tmp_path):
    # Try reading a directory instead of a file
    dir_path = tmp_path / "folder"
    dir_path.mkdir()
    with pytest.raises(StorageReadError):
        read_json(dir_path)
