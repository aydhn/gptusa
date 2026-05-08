from usa_signal_bot.observability.metrics_collector import OperationalMetricsCollector
from pathlib import Path
import tempfile

def test_metrics_collector():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td)
        c = OperationalMetricsCollector(p)
        snap = c.collect_all()
        assert len(snap.metrics) > 0
        # should be warning because missing dirs
        assert snap.status.value == "WARNING"
