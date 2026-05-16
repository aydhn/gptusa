from usa_signal_bot.portfolio_construction.sector_cluster_registry import write_sector_cluster_registry_example, load_sector_cluster_registry
from pathlib import Path

def test_write_and_load_registry(tmp_path):
    p = tmp_path / "registry.json"
    write_sector_cluster_registry_example(p)
    assert p.exists()
    records = load_sector_cluster_registry(p)
    assert len(records) > 0
    assert records[0].symbol == "AAPL"
