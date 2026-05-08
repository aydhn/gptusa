from usa_signal_bot.release.upgrade_precheck import run_upgrade_precheck
from pathlib import Path

def test_run_upgrade_precheck(tmp_path):
    res = run_upgrade_precheck(tmp_path, tmp_path / "data")
    # Will likely have some warnings (missing requirements, config)
    assert res.status.value in ["PASSED", "WARNING"]
