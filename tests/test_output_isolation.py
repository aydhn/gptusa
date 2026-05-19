import pytest
from pathlib import Path
from usa_signal_bot.core.exceptions import SandboxOutputIsolationError
from usa_signal_bot.release_sandbox.output_isolation import (
    sandbox_output_root, sandbox_output_dir, validate_sandbox_output_path,
    write_sandbox_output_json, write_sandbox_output_text, output_isolation_summary
)

def test_output_isolation_dirs(tmp_path):
    root = sandbox_output_root(tmp_path)
    assert root.name == "outputs"

    s_dir = sandbox_output_dir(tmp_path, "s1")
    assert s_dir.name == "s1"
    assert s_dir.parent == root

def test_validate_output_path(tmp_path):
    root = sandbox_output_root(tmp_path)
    safe_path = root / "s1" / "out.json"

    warns = validate_sandbox_output_path(safe_path, tmp_path)
    assert not warns

    unsafe_path = tmp_path / "not_outputs" / "out.json"
    warns = validate_sandbox_output_path(unsafe_path, tmp_path)
    assert len(warns) > 0
    assert "Path traversal" in warns[0]

def test_write_sandbox_outputs(tmp_path):
    safe_path = tmp_path / "release_sandbox" / "outputs" / "out.json"
    safe_path.parent.mkdir(parents=True, exist_ok=True)
    write_sandbox_output_json(safe_path, {"key": "val"})
    assert safe_path.exists()

    safe_txt = tmp_path / "release_sandbox" / "outputs" / "out.txt"
    write_sandbox_output_text(safe_txt, "hello")
    assert safe_txt.exists()

    unsafe_path = tmp_path / "not_outputs" / "out.json"
    with pytest.raises(SandboxOutputIsolationError):
        write_sandbox_output_json(unsafe_path, {"key": "val"})
