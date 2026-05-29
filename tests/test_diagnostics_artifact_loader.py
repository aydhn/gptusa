from pathlib import Path
from usa_signal_bot.regime_classification.behavior_reporting.diagnostics_artifact_loader import (
    validate_diagnostics_artifact_payloads, load_transition_matrices_jsonl
)

def test_validate_diagnostics_artifact_payloads():
    payloads = {
        "matrices": [
            {"api_key": "123"},
            {"valid": "data"}
        ]
    }
    errs = validate_diagnostics_artifact_payloads(payloads)
    assert len(errs) > 0
    assert "api_key" in errs[0]

def test_load_transition_matrices_jsonl(tmp_path):
    f = tmp_path / "test.jsonl"
    f.write_text('{"a": 1}\n{"b": 2}')
    res = load_transition_matrices_jsonl(f)
    assert len(res) == 2
