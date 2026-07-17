import pytest
import json
from pathlib import Path
from usa_signal_bot.release_sandbox.bundle_loader import (
    load_bundle_for_sandbox, load_bundle_manifest_for_sandbox, bundle_loader_to_text, load_bundle_artifacts_for_sandbox
)

def test_load_bundle_missing_path(tmp_path):
    bundle_path = tmp_path / "missing.json"
    res = load_bundle_for_sandbox(bundle_path)
    assert "error" in res
    assert res["error"] == "Bundle not found."

def test_load_bundle_valid(tmp_path):
    bundle_path = tmp_path / "bundle.json"
    bundle_data = {
        "manifest": {"bundle_id": "b1", "bundle_version": "v1"},
        "artifacts": [{"name": "art1"}],
        "validation": {"status": "PASS"}
    }
    with open(bundle_path, "w") as f:
        json.dump(bundle_data, f)

    res = load_bundle_for_sandbox(bundle_path)
    assert res["manifest"]["bundle_id"] == "b1"

    man = load_bundle_manifest_for_sandbox(bundle_path)
    assert man["bundle_version"] == "v1"

    artifacts = load_bundle_artifacts_for_sandbox(bundle_path)
    assert len(artifacts) == 1
    assert artifacts[0]["name"] == "art1"

    txt = bundle_loader_to_text(res)
    assert "ID=b1" in txt
    assert "Artifacts=1" in txt

def test_load_bundle_invalid_json(tmp_path):
    bundle_path = tmp_path / "invalid.json"
    with open(bundle_path, "w") as f:
        f.write("{invalid_json}")

    with pytest.raises(json.JSONDecodeError):
        load_bundle_for_sandbox(bundle_path)

def test_bundle_loader_to_text_edge_cases():
    empty_payload = {}
    txt = bundle_loader_to_text(empty_payload)
    assert txt == "Bundle Loaded: ID=unknown, Version=unknown, Artifacts=0"

    manifest_only = {"manifest": {"bundle_id": "test-123", "bundle_version": "v1.2"}}
    txt2 = bundle_loader_to_text(manifest_only)
    assert txt2 == "Bundle Loaded: ID=test-123, Version=v1.2, Artifacts=0"

    artifacts_only = {"artifacts": [{"name": "a1"}, {"name": "a2"}]}
    txt3 = bundle_loader_to_text(artifacts_only)
    assert txt3 == "Bundle Loaded: ID=unknown, Version=unknown, Artifacts=2"
