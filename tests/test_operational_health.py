from usa_signal_bot.observability.operational_health import OperationalHealthEvaluator
import tempfile
from pathlib import Path

def test_operational_health():
    with tempfile.TemporaryDirectory() as td:
        e = OperationalHealthEvaluator(Path(td))
        r = e.build_report()
        assert r.status.value in ["HEALTHY", "WARNING", "CRITICAL", "FAILED"]
