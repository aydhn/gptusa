import json

import pytest

from usa_signal_bot.paper_common import (
    ValidationIssue, ValidationReport, append_jsonl, count_files, ensure_dir,
    latest_by_mtime, list_files, read_json, read_jsonl, write_json, write_jsonl,
)


def test_ensure_dir_creates_and_is_idempotent(tmp_path):
    d = tmp_path / "a" / "b"
    assert ensure_dir(d) == d and d.is_dir()
    assert ensure_dir(d) == d


def test_write_json_roundtrip_creates_parent_and_indent(tmp_path):
    p = tmp_path / "x" / "y.json"
    assert write_json(p, {"b": 1, "a": [1, 2]}) == p
    assert read_json(p) == {"b": 1, "a": [1, 2]}
    assert p.read_text() == json.dumps({"b": 1, "a": [1, 2]}, indent=2)


def test_write_json_no_parent_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        write_json(tmp_path / "missing" / "y.json", {}, ensure_parent=False)


def test_read_json_missing_and_empty(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_json(tmp_path / "nope.json")
    e = tmp_path / "e.json"
    e.write_text("")
    with pytest.raises(json.JSONDecodeError):
        read_json(e)


def test_jsonl_roundtrip_overwrite_and_append(tmp_path):
    p = tmp_path / "d" / "r.jsonl"
    write_jsonl(p, ({"i": i} for i in range(2)))
    assert read_jsonl(p) == [{"i": 0}, {"i": 1}]
    write_jsonl(p, [{"i": 9}])
    assert read_jsonl(p) == [{"i": 9}]
    append_jsonl(p, [{"i": 10}])
    assert read_jsonl(p) == [{"i": 9}, {"i": 10}]


def test_jsonl_empty_and_missing(tmp_path):
    p = tmp_path / "e.jsonl"
    write_jsonl(p, [])
    assert p.read_text() == ""
    assert read_jsonl(p) == []
    p.write_text('{"a": 1}\n\n')
    assert read_jsonl(p) == [{"a": 1}]
    with pytest.raises(FileNotFoundError):
        read_jsonl(tmp_path / "nope.jsonl")


def test_list_count_latest(tmp_path):
    assert list_files(tmp_path / "none", "*.json") == []
    assert count_files(tmp_path / "none") == 0
    assert latest_by_mtime([]) is None
    for n in ("b.json", "a.json", "c.txt"):
        (tmp_path / n).write_text("{}")
    assert list_files(tmp_path, "*.json", sort=True) == [tmp_path / "a.json", tmp_path / "b.json"]
    assert list_files(tmp_path, "*.json", reverse=True) == [tmp_path / "b.json", tmp_path / "a.json"]
    assert count_files(tmp_path, "*.*") == 3
    import os
    os.utime(tmp_path / "a.json", (1, 1))
    os.utime(tmp_path / "b.json", (2, 2))
    assert latest_by_mtime(list_files(tmp_path, "*.json")) == tmp_path / "b.json"


def test_validation_types_defaults():
    i = ValidationIssue("ERROR", None, "m")
    assert i.details == {}
    r = ValidationReport(True, 0, 0, 0, 0, [], [], [])
    assert r.valid and r.issues == []
