import json
from pathlib import Path
from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_scaffolding_artifact_loader import validate_ensemble_scaffolding_artifacts

def test_validate_ensemble_scaffolding_artifacts():
    payloads = {
        "reports": [{"deployment_allowed": True}]
    }
    errors = validate_ensemble_scaffolding_artifacts(payloads)
    assert len(errors) == 1
    assert "Unsafe flags in reports[0]" in errors[0]
