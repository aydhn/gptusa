import pytest
from pathlib import Path
from usa_signal_bot.regression.golden_snapshots import (
    create_golden_snapshot, stable_payload_checksum, normalize_payload_for_snapshot,
    write_golden_snapshot_json, read_golden_snapshot_json, compare_golden_snapshots,
    write_or_update_baseline_snapshot
)
from usa_signal_bot.regression.regression_models import RegressionArtifactType

def test_stable_payload_checksum():
    p1 = {"a": 1, "b": [1, 2]}
    p2 = {"b": [1, 2], "a": 1}
    assert stable_payload_checksum(p1) == stable_payload_checksum(p2)

def test_normalize_payload():
    payload = {
        "data": 123,
        "run_id": "r123",
        "nested": {
            "timestamp": "now",
            "val": 1
        }
    }
    norm = normalize_payload_for_snapshot(payload)
    assert "data" in norm
    assert "run_id" not in norm
    assert "timestamp" not in norm["nested"]
    assert "val" in norm["nested"]

def test_create_and_rw_snapshot(tmp_path):
    snap = create_golden_snapshot("test", {"a": 1})
    assert snap.name == "test"

    p = tmp_path / "snap.json"
    write_golden_snapshot_json(p, snap)

    read_snap = read_golden_snapshot_json(p)
    assert read_snap.checksum == snap.checksum
    assert read_snap.payload == snap.payload

def test_compare_golden_snapshots():
    s1 = create_golden_snapshot("test", {"a": 1})
    s2 = create_golden_snapshot("test", {"a": 1})

    comp = compare_golden_snapshots(s1, s2)
    assert comp["status"] == "MATCH"

    s3 = create_golden_snapshot("test", {"a": 2})
    comp2 = compare_golden_snapshots(s1, s3)
    assert comp2["status"] == "DRIFT"
    assert comp2["diff_summary"]["diff_count"] > 0

    comp3 = compare_golden_snapshots(None, s2)
    assert comp3["status"] == "MISSING_BASELINE"

def test_write_or_update_baseline_snapshot(tmp_path):
    snap1 = create_golden_snapshot("test", {"a": 1})
    p = write_or_update_baseline_snapshot(tmp_path, snap1, update=False)
    assert p.exists()

    snap2 = create_golden_snapshot("test", {"a": 2})
    # update=False should not overwrite
    p2 = write_or_update_baseline_snapshot(tmp_path, snap2, update=False)

    read_s = read_golden_snapshot_json(p)
    assert read_s.checksum == snap1.checksum

    # update=True should overwrite
    write_or_update_baseline_snapshot(tmp_path, snap2, update=True)
    read_s2 = read_golden_snapshot_json(p)
    assert read_s2.checksum == snap2.checksum
