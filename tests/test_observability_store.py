from usa_signal_bot.observability.observability_store import observability_store_summary
import tempfile
from pathlib import Path

def test_observability_store():
    with tempfile.TemporaryDirectory() as td:
        s = observability_store_summary(Path(td))
        assert s["logs"] == 0
