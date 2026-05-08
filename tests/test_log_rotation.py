import tempfile
from pathlib import Path
from usa_signal_bot.observability.log_rotation import LogRotationManager, LogRotationConfig

def test_log_rotation():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "events.log"
        p.write_text("a\n" * 10)

        config = LogRotationConfig(max_file_size_bytes=5)
        mgr = LogRotationManager(config)

        res = mgr.rotate_if_needed(p)
        assert res.status.value == "ROTATED"
        assert res.rotated_path is not None
        assert not p.exists() or p.stat().st_size == 0

        # dry run
        p.write_text("a\n" * 10)
        config.dry_run = True
        mgr2 = LogRotationManager(config)
        res2 = mgr2.rotate_if_needed(p)
        assert res2.status.value == "NOT_NEEDED"
