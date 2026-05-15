import pytest
import tempfile
from pathlib import Path
from usa_signal_bot.regime_costs.regime_cost_store import (
    write_cost_regime_snapshot_json, regime_cost_store_summary
)
from usa_signal_bot.regime_costs.combined_regime_classifier import build_cost_regime_snapshot

def test_regime_cost_store():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        s = build_cost_regime_snapshot("SPY")

        from usa_signal_bot.regime_costs.regime_cost_store import regime_snapshots_dir
        sp = regime_snapshots_dir(root) / "test.json"

        write_cost_regime_snapshot_json(sp, s)
        assert sp.exists()

        sum = regime_cost_store_summary(root)
        assert sum["reviews_count"] == 0
