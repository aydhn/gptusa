import pytest
from pathlib import Path
from usa_signal_bot.ml_research.ensemble_scaffolding.calibration_diagnostics_artifact_loader import (
    load_calibration_diagnostics_reports_jsonl,
    validate_calibration_diagnostics_artifacts
)

def test_load_reports():
    p = Path("tests/fixtures/ml_ensemble_scaffolding/sample_calibration_diagnostics_reports.jsonl")
    res = load_calibration_diagnostics_reports_jsonl(p)
    assert len(res) == 2
    assert res[0]['candidate_id'] == "cand_1"

def test_validate_artifacts():
    payloads = {
        "bad_obj": {"live_inference_enabled": True}
    }
    errs = validate_calibration_diagnostics_artifacts(payloads)
    assert len(errs) > 0
    assert "live_inference_enabled in bad_obj" in errs
