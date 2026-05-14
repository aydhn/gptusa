import pytest
from pathlib import Path
from usa_signal_bot.transaction_costs.cost_store import cost_store_dir, cost_breakdowns_dir

def test_cost_store_dirs(tmp_path):
    assert cost_store_dir(tmp_path).exists()
    assert cost_breakdowns_dir(tmp_path).exists()
