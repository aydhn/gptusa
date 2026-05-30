import pytest
from usa_signal_bot.regime_classification.validation.alignment_artifact_loader import validate_alignment_artifacts

def test_validate_alignment_artifacts_safe():
    payloads = {
        "score": 90,
        "classification": "high"
    }
    errs = validate_alignment_artifacts(payloads)
    assert len(errs) == 0

def test_validate_alignment_artifacts_unsafe():
    payloads = {
        "score": 90,
        "buy_signal_confirmed": True
    }
    errs = validate_alignment_artifacts(payloads)
    assert len(errs) > 0
    assert any("Unsafe field" in e for e in errs)
