from usa_signal_bot.observability.artifact_metrics import collect_artifact_metrics
import tempfile
from pathlib import Path

def test_artifact_metrics():
    with tempfile.TemporaryDirectory() as td:
        s = collect_artifact_metrics(Path(td))
        assert len(s.missing_artifacts) > 0
