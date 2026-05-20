import pytest
from pathlib import Path
from usa_signal_bot.core.exceptions import QuarantineOutputIsolationError
from usa_signal_bot.paper_quarantine.output_isolation import (
    quarantine_output_root,
    quarantine_output_dir,
    validate_quarantine_output_path,
    write_quarantine_output_json,
    write_quarantine_output_text,
)

def test_root():
    root = quarantine_output_root(Path("/data"))
    assert str(root) == "/data/paper_quarantine/outputs"

def test_dir():
    d = quarantine_output_dir(Path("/data"), "c1")
    assert str(d) == "/data/paper_quarantine/outputs/c1"

def test_valid_path():
    data_root = Path("/data")
    path = quarantine_output_dir(data_root, "c1") / "out.json"
    assert not validate_quarantine_output_path(path, data_root)

def test_invalid_path():
    data_root = Path("/data")
    path = data_root / "paper" / "state.json"
    assert len(validate_quarantine_output_path(path, data_root)) > 0

def test_write(tmp_path):
    data_root = tmp_path / "data"
    path = quarantine_output_dir(data_root, "c1") / "out.json"
    write_quarantine_output_json(path, {"a": 1}, data_root)
    assert path.exists()

def test_write_invalid(tmp_path):
    data_root = tmp_path / "data"
    path = data_root / "paper" / "state.json"
    with pytest.raises(QuarantineOutputIsolationError):
        write_quarantine_output_json(path, {"a": 1}, data_root)
