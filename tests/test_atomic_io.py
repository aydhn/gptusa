import pytest
import tempfile
import json
from pathlib import Path

from usa_signal_bot.scheduler.atomic_io import (
    atomic_write_text, atomic_write_json, atomic_write_jsonl, safe_replace, atomic_write_result_to_text
)
from usa_signal_bot.core.enums import AtomicWriteStatus

def test_atomic_write_text():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "test.txt"
        res = atomic_write_text(p, "hello world")
        assert res.status == AtomicWriteStatus.WRITTEN
        assert res.bytes_written > 0
        assert p.exists()
        with open(p, "r") as f:
            assert f.read() == "hello world"

def test_atomic_write_json():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "test.json"
        res = atomic_write_json(p, {"a": 1})
        assert res.status == AtomicWriteStatus.WRITTEN
        with open(p, "r") as f:
            data = json.load(f)
        assert data["a"] == 1

def test_atomic_write_jsonl():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "test.jsonl"
        res = atomic_write_jsonl(p, [{"a": 1}, {"b": 2}])
        assert res.status == AtomicWriteStatus.WRITTEN
        with open(p, "r") as f:
            lines = f.readlines()
        assert len(lines) == 2

def test_safe_replace():
    with tempfile.TemporaryDirectory() as td:
        p1 = Path(td) / "src.txt"
        p2 = Path(td) / "dst.txt"

        with open(p1, "w") as f:
            f.write("hello")

        res = safe_replace(p1, p2)
        assert res.status == AtomicWriteStatus.REPLACED
        assert p2.exists()
        assert not p1.exists()

def test_atomic_result_text():
    res = atomic_write_text(Path("dummy.txt"), "hello")
    txt = atomic_write_result_to_text(res)
    assert "AtomicWrite" in txt
