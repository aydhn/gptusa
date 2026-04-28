import pytest
from usa_signal_bot.storage.file_store import LocalFileStore
from usa_signal_bot.core.exceptions import StoragePathError

def test_file_store_lifecycle(tmp_path):
    store = LocalFileStore(tmp_path)
    store.ensure_ready()

    # JSON test
    store.write_json("cache", "test.json", {"key": "value"})
    assert store.exists("cache", "test.json")
    data = store.read_json("cache", "test.json")
    assert data["key"] == "value"

    # JSONL test
    store.append_jsonl("logs", "test.jsonl", {"event": 1})
    store.append_jsonl("logs", "test.jsonl", {"event": 2})
    records = store.read_jsonl("logs", "test.jsonl")
    assert len(records) == 2

    # CSV test
    store.write_csv("reports", "test.csv", [{"id": 1}], fieldnames=["id"])
    csv_data = store.read_csv("reports", "test.csv")
    assert len(csv_data) == 1

    # List files
    files = store.list_files("logs")
    assert len(files) == 1
    assert files[0].name == "test.jsonl"

    # Delete
    store.delete("cache", "test.json")
    assert not store.exists("cache", "test.json")

def test_file_store_path_traversal(tmp_path):
    store = LocalFileStore(tmp_path)

    from usa_signal_bot.core.exceptions import PathError
    with pytest.raises(PathError):
        store.path("cache", "../escaped.json")

    # Attempt delete outside root
    outside_file = tmp_path.parent / "outside.txt"
    from usa_signal_bot.core.exceptions import PathError
    with pytest.raises(PathError):
        store.delete("cache", "../../../outside.txt")
