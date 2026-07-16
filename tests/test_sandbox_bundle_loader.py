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
