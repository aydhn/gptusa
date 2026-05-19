import pytest
from pathlib import Path
from usa_signal_bot.paper_shadow.shadow_store import (
    shadow_store_summary
)
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context
from usa_signal_bot.paper_shadow.shadow_store import write_shadow_context_json

def test_shadow_store(tmp_path):
    ctx = build_mock_shadow_simulation_context()
    path = tmp_path / "paper_shadow" / "contexts" / "test.json"
    write_shadow_context_json(path, ctx)
    assert path.exists()

    summ = shadow_store_summary(tmp_path)
    assert summ["contexts_count"] == 1
