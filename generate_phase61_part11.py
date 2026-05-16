import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"Created {path}")

# --- Tests ---

write_file("tests/test_portfolio_models.py", """import pytest
from usa_signal_bot.portfolio_construction.portfolio_models import SectorClusterRecord, PortfolioCandidate, validate_sector_cluster_record
from usa_signal_bot.core.enums import SectorClusterSource

def test_sector_cluster_record_valid():
    rec = SectorClusterRecord("id1", "AAPL", "tech", "hw", "mega", SectorClusterSource.MANUAL_REGISTRY, 100.0)
    assert rec.symbol == "AAPL"

def test_sector_cluster_record_invalid():
    rec = SectorClusterRecord("id1", "", "tech", "hw", "mega", SectorClusterSource.MANUAL_REGISTRY, 100.0)
    with pytest.raises(ValueError):
        validate_sector_cluster_record(rec)
""")

write_file("tests/test_sector_cluster_registry.py", """from usa_signal_bot.portfolio_construction.sector_cluster_registry import write_sector_cluster_registry_example, load_sector_cluster_registry
from pathlib import Path

def test_write_and_load_registry(tmp_path):
    p = tmp_path / "registry.json"
    write_sector_cluster_registry_example(p)
    assert p.exists()
    records = load_sector_cluster_registry(p)
    assert len(records) > 0
    assert records[0].symbol == "AAPL"
""")

write_file("tests/test_sector_cluster_resolver.py", """from usa_signal_bot.portfolio_construction.sector_cluster_resolver import SectorClusterResolver
from usa_signal_bot.portfolio_construction.portfolio_models import SectorClusterRecord
from usa_signal_bot.core.enums import SectorClusterSource

def test_resolver_etf_proxy():
    resolver = SectorClusterResolver([])
    rec = resolver.resolve("SPY")
    assert rec.sector == "broad_market"
    assert rec.source == SectorClusterSource.ETF_PROXY_HEURISTIC

def test_resolver_unknown():
    resolver = SectorClusterResolver([])
    rec = resolver.resolve("UNKNOWN_TICKER")
    assert rec.sector == "unknown_sector"
    assert rec.source == SectorClusterSource.UNKNOWN
""")

write_file("tests/test_exposure_calculator.py", """from usa_signal_bot.portfolio_construction.exposure_calculator import calculate_exposure_snapshot
from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioAllocation

def test_calculate_exposure():
    allocs = [
        PortfolioAllocation("1", "AAPL", "T", "LONG", 100, 100, 1, 10, "APPROVED", [], [], [], []),
        PortfolioAllocation("2", "TSLA", "T", "SHORT", 50, 50, 1, 5, "APPROVED", [], [], [], [])
    ]
    snap = calculate_exposure_snapshot(allocs, 1000)
    assert snap.gross_exposure_usd == 150
    assert snap.long_exposure_usd == 100
    assert snap.short_exposure_usd == -50
    assert snap.net_exposure_usd == 50
""")

write_file("tests/test_exposure_limits.py", """from usa_signal_bot.portfolio_construction.exposure_limits import check_gross_exposure_limit
from usa_signal_bot.portfolio_construction.exposure_calculator import calculate_exposure_snapshot

def test_gross_limit_clear():
    snap = calculate_exposure_snapshot([{"final_notional_usd": 50}], 100)
    res = check_gross_exposure_limit(snap, 100.0)
    assert res.decision.value == "CLEAR"

def test_gross_limit_block():
    snap = calculate_exposure_snapshot([{"final_notional_usd": 150}], 100)
    res = check_gross_exposure_limit(snap, 100.0)
    assert res.decision.value == "BLOCK"
""")

write_file("tests/test_concentration_guards.py", """from usa_signal_bot.portfolio_construction.concentration_guards import assess_symbol_concentration
from usa_signal_bot.portfolio_construction.exposure_calculator import calculate_exposure_snapshot

def test_symbol_concentration_clear():
    snap = calculate_exposure_snapshot([{"symbol": "AAPL", "final_notional_usd": 5}], 100)
    res = assess_symbol_concentration(snap, 10.0)
    assert res[0].decision.value == "CLEAR"

def test_symbol_concentration_cap():
    snap = calculate_exposure_snapshot([{"symbol": "AAPL", "final_notional_usd": 15}], 100)
    res = assess_symbol_concentration(snap, 10.0)
    assert res[0].decision.value == "BLOCK"
""")

write_file("tests/test_correlation_proxy.py", """from usa_signal_bot.portfolio_construction.correlation_proxy import estimate_pairwise_correlation_proxy

def test_correlation_proxy():
    assert estimate_pairwise_correlation_proxy("AAPL", "AAPL").value == "VERY_HIGH"
    assert estimate_pairwise_correlation_proxy("AAPL", "MSFT", {"cluster": "tech"}, {"cluster": "tech"}).value == "HIGH"
""")

write_file("tests/test_allocation_planner.py", """from usa_signal_bot.portfolio_construction.allocation_planner import PortfolioAllocationPlanner
from usa_signal_bot.core.enums import PortfolioConstructionMode

def test_equal_weight():
    planner = PortfolioAllocationPlanner(mode=PortfolioConstructionMode.EQUAL_WEIGHT)
    cands = planner.build_candidates([{"symbol": "AAPL"}, {"symbol": "MSFT"}])
    allocs = planner.plan_allocations(cands, 1000)
    assert allocs[0].final_notional_usd == 500
    assert allocs[1].final_notional_usd == 500
""")

write_file("tests/test_portfolio_balancer.py", """from usa_signal_bot.portfolio_construction.portfolio_balancer import PortfolioBalancer
from usa_signal_bot.portfolio_construction.allocation_planner import PortfolioAllocationPlanner

def test_balancer_build_plan():
    planner = PortfolioAllocationPlanner()
    cands = planner.build_candidates([{"symbol": "AAPL"}])
    balancer = PortfolioBalancer()
    plan = balancer.build_plan(cands, 1000)
    assert plan.approved_count == 1
    assert plan.total_allocated_notional_usd > 0
""")

write_file("tests/test_cli_portfolio.py", """import pytest
from click.testing import CliRunner
from usa_signal_bot.app.cli import cli

def test_portfolio_info():
    runner = CliRunner()
    res = runner.invoke(cli, ["portfolio-construction-info"])
    assert res.exit_code == 0
    assert "Portfolio Construction" in res.output

def test_sector_example():
    runner = CliRunner()
    with runner.isolated_filesystem():
        res = runner.invoke(cli, ["sector-cluster-write-example"])
        assert res.exit_code == 0
""")

print("Generated step 11")
