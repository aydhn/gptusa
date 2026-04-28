import pytest
from usa_signal_bot.storage.integrity import sha256_file, file_size_bytes, validate_file_exists, validate_file_under_root, build_file_metadata
from usa_signal_bot.core.exceptions import StorageIntegrityError, StoragePathError
from usa_signal_bot.utils.hash_utils import sha256_text

def test_file_integrity(tmp_path):
    file_path = tmp_path / "test.txt"
    content = "hello integrity"
    file_path.write_text(content)

    expected_hash = sha256_text(content)

    assert sha256_file(file_path) == expected_hash
    assert file_size_bytes(file_path) == len(content)

def test_validate_file_exists(tmp_path):
    missing_file = tmp_path / "missing.txt"
    with pytest.raises(StorageIntegrityError):
        validate_file_exists(missing_file)

def test_validate_file_under_root(tmp_path):
    root_dir = tmp_path / "data"
    root_dir.mkdir()

    valid_file = root_dir / "valid.txt"
    valid_file.touch()

    invalid_file = tmp_path / "escaped.txt"
    invalid_file.touch()

    validate_file_under_root(valid_file, root_dir) # Should pass

    with pytest.raises(StoragePathError):
        validate_file_under_root(invalid_file, root_dir)

def test_build_file_metadata(tmp_path):
    file_path = tmp_path / "meta.txt"
    file_path.write_text("test")

    meta = build_file_metadata(file_path)
    assert "size_bytes" in meta
    assert "sha256" in meta
    assert "modified_at" in meta
    assert meta["size_bytes"] == 4
