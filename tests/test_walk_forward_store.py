from pathlib import Path
from usa_signal_bot.backtesting.walk_forward_store import (
    build_walk_forward_run_dir, walk_forward_store_dir, list_walk_forward_runs
)

def test_store_dirs(tmp_path):
    d = walk_forward_store_dir(tmp_path)
    assert d.exists()

    rd = build_walk_forward_run_dir(tmp_path, "wf_test_123")
    assert rd.exists()

    runs = list_walk_forward_runs(tmp_path)
    assert len(runs) == 1
