from usa_signal_bot.observability.disk_usage import collect_disk_usage_summary
import tempfile
from pathlib import Path

def test_disk_usage():
    with tempfile.TemporaryDirectory() as td:
        s = collect_disk_usage_summary(Path(td))
        assert s.path == td
        assert s.status.value in ["OK", "WARNING", "CRITICAL"] # depending on machine
