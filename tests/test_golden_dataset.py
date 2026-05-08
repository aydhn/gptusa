import pytest
from pathlib import Path
import json
from usa_signal_bot.regression.golden_dataset import GoldenDatasetManager
from usa_signal_bot.regression.regression_models import GoldenDatasetStatus

def test_default_spec(tmp_path):
    mgr = GoldenDatasetManager(tmp_path)
    spec = mgr.default_spec()
    assert spec.name == "golden_small_us"
    assert "SPY" in spec.symbols

def test_create_and_validate_dataset(tmp_path):
    mgr = GoldenDatasetManager(tmp_path)
    spec = mgr.default_spec()
    spec.name = "test_create"

    paths = mgr.create_dataset(spec, overwrite=True)
    assert "manifest" in paths

    valid, warnings, errors = mgr.validate_dataset(spec)
    assert valid is True
    assert len(errors) == 0

def test_validate_missing_files_dataset(tmp_path):
    mgr = GoldenDatasetManager(tmp_path)
    spec = mgr.default_spec()
    spec.name = "test_missing"

    # create partial dataset
    ds_dir = mgr.dataset_dir(spec.name)
    ds_dir.mkdir(parents=True)
    with open(ds_dir / "manifest.json", "w") as f:
        f.write('{"spec": {"symbols": ["AAPL"]}, "paths": {}}')

    valid, warnings, errors = mgr.validate_dataset(spec)
    assert valid is False
    assert len(errors) > 0
    assert any("Missing OHLCV" in e for e in errors)

def test_dataset_dirs(tmp_path):
    mgr = GoldenDatasetManager(tmp_path)
    d1 = mgr.dataset_dir("test1")
    assert d1.name == "test1"
    assert mgr.latest_dataset_dir() is None

    mgr.create_dataset(overwrite=True)
    latest = mgr.latest_dataset_dir()
    assert latest is not None

def test_manifest_read_write(tmp_path):
    mgr = GoldenDatasetManager(tmp_path)
    spec = mgr.default_spec()
    ds_dir = mgr.dataset_dir(spec.name)
    ds_dir.mkdir(parents=True, exist_ok=True)
    mgr.write_dataset_manifest(spec, {"test": "path"})

    man = mgr.load_dataset_manifest(spec.name)
    assert man is not None
    assert "test" in man["paths"]

def test_install_dataset_into_local_cache(tmp_path):
    mgr = GoldenDatasetManager(tmp_path)
    spec = mgr.default_spec()
    mgr.create_dataset(spec, overwrite=True)

    installed = mgr.install_dataset_into_local_cache(spec.name, tmp_path / "cache")
    assert len(installed) > 0
    assert "signals.jsonl" in installed
