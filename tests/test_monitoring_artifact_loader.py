import pytest
from pathlib import Path
from usa_signal_bot.regime_classification.freeze_preparation.monitoring_artifact_loader import (
    load_monitoring_baseline_json,
    validate_monitoring_artifacts
)
from usa_signal_bot.core.exceptions import MonitoringArtifactLoaderError

def test_load_baseline(tmp_path):
    f = tmp_path / "baseline.json"
    f.write_text('{"id": "base1"}')
    res = load_monitoring_baseline_json(f)
    assert res["id"] == "base1"

def test_load_baseline_missing():
    with pytest.raises(MonitoringArtifactLoaderError):
        load_monitoring_baseline_json(Path("does_not_exist.json"))

def test_validate_monitoring_artifacts_safe():
    payloads = {"data": "safe text"}
    errors = validate_monitoring_artifacts(payloads)
    assert len(errors) == 0

def test_validate_monitoring_artifacts_unsafe():
    payloads = {"data": "kesin al"}
    errors = validate_monitoring_artifacts(payloads)
    assert len(errors) > 0
