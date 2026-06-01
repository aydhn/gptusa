import pytest
import json
from pathlib import Path
from usa_signal_bot.ml_research.ensemble_scaffolding.calibration_diagnostics_ingestion import ingest_calibration_diagnostics_review_payload

def test_ingest_pass(tmp_path):
    p = Path("tests/fixtures/ml_ensemble_scaffolding/sample_calibration_diagnostics_review.json")
    with open(p, "r") as f:
        data = json.load(f)

    res = ingest_calibration_diagnostics_review_payload(data)
    assert res.valid_for_phase142 is True
    assert res.ready_for_phase142 is True
    assert len(res.errors) == 0

def test_ingest_blocked(tmp_path):
    p = Path("tests/fixtures/ml_ensemble_scaffolding/sample_calibration_diagnostics_review_blocked.json")
    with open(p, "r") as f:
        data = json.load(f)

    res = ingest_calibration_diagnostics_review_payload(data)
    assert res.valid_for_phase142 is False
    assert len(res.errors) > 0
