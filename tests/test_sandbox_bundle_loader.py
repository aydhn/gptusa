import pytest
import json
from pathlib import Path
from usa_signal_bot.release_sandbox.bundle_loader import (
    load_bundle_for_sandbox,
    load_bundle_manifest_for_sandbox,
    bundle_loader_to_text,
    bundle_loader_summary,
)


def test_load_bundle_missing_path(tmp_path):
    bundle_path = tmp_path / "missing.json"
    res = load_bundle_for_sandbox(bundle_path)
    assert "error" in res


def test_load_bundle_valid(tmp_path):
    bundle_path = tmp_path / "bundle.json"
    bundle_data = {
        "manifest": {"bundle_id": "b1", "bundle_version": "v1"},
        "artifacts": [{"name": "art1"}],
        "validation": {"status": "PASS"},
    }
    with open(bundle_path, "w") as f:
        json.dump(bundle_data, f)

    res = load_bundle_for_sandbox(bundle_path)
    assert res["manifest"]["bundle_id"] == "b1"

    man = load_bundle_manifest_for_sandbox(bundle_path)
    assert man["bundle_version"] == "v1"

    txt = bundle_loader_to_text(res)
    assert "ID=b1" in txt
    assert "Artifacts=1" in txt


def test_bundle_loader_summary():
    valid_payload = {
        "manifest": {"bundle_id": "b1", "bundle_version": "v1"},
        "artifacts": [{"name": "art1"}, {"name": "art2"}],
        "validation": {"status": "PASS"},
    }
    res_valid = bundle_loader_summary(valid_payload)
    assert res_valid["bundle_id"] == "b1"
    assert res_valid["bundle_version"] == "v1"
    assert res_valid["artifact_count"] == 2
    assert res_valid["validation_present"] is True

    empty_payload = {}
    res_empty = bundle_loader_summary(empty_payload)
    assert res_empty["bundle_id"] == "unknown"
    assert res_empty["bundle_version"] == "unknown"
    assert res_empty["artifact_count"] == 0
    assert res_empty["validation_present"] is False
