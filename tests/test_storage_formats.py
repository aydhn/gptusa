import pytest
from usa_signal_bot.storage.formats import StorageFormat, extension_for_format, format_from_extension, ensure_supported_format
from usa_signal_bot.core.exceptions import UnsupportedOperationError

def test_extensions():
    assert extension_for_format(StorageFormat.JSON) == ".json"
    assert extension_for_format(StorageFormat.JSONL) == ".jsonl"
    assert extension_for_format(StorageFormat.CSV) == ".csv"

def test_format_from_extension():
    assert format_from_extension("json") == StorageFormat.JSON
    assert format_from_extension(".jsonl") == StorageFormat.JSONL
    assert format_from_extension(".CSV") == StorageFormat.CSV

def test_ensure_supported_format():
    # Should not raise
    ensure_supported_format(StorageFormat.JSON)
    ensure_supported_format(StorageFormat.JSONL)
    ensure_supported_format(StorageFormat.CSV)

    with pytest.raises(UnsupportedOperationError):
        ensure_supported_format(StorageFormat.PARQUET_RESERVED)
