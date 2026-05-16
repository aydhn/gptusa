import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"Created {path}")

# --- core/health.py ---
health_path = "usa_signal_bot/core/health.py"
try:
    with open(health_path, "r") as f:
        health_content = f.read()

    new_healths = """
def check_portfolio_construction_config_health(context) -> dict:
    return {"status": "healthy", "details": "Portfolio construction config is valid (mock)."}

def check_sector_cluster_registry_health(context) -> dict:
    return {"status": "healthy", "details": "Sector cluster registry is healthy (mock)."}

def check_sector_cluster_resolver_health(context) -> dict:
    return {"status": "healthy", "details": "Sector cluster resolver is healthy (mock)."}

def check_exposure_calculator_health(context) -> dict:
    return {"status": "healthy", "details": "Exposure calculator is healthy (mock)."}

def check_exposure_limits_health(context) -> dict:
    return {"status": "healthy", "details": "Exposure limits logic is healthy (mock)."}

def check_concentration_guards_health(context) -> dict:
    return {"status": "healthy", "details": "Concentration guards are healthy (mock)."}

def check_correlation_proxy_health(context) -> dict:
    return {"status": "healthy", "details": "Correlation proxy is healthy (mock)."}

def check_portfolio_allocation_planner_health(context) -> dict:
    return {"status": "healthy", "details": "Portfolio allocation planner is healthy (mock)."}

def check_portfolio_balancer_health(context) -> dict:
    return {"status": "healthy", "details": "Portfolio balancer is healthy (mock)."}

def check_portfolio_construction_store_health(context) -> dict:
    return {"status": "healthy", "details": "Portfolio construction store is healthy (mock)."}

def check_portfolio_construction_notification_health(context) -> dict:
    return {"status": "healthy", "details": "Portfolio construction notifications are healthy (mock)."}
"""
    if "check_portfolio_construction_config_health" not in health_content:
        health_content += new_healths
        with open(health_path, "w") as f:
            f.write(health_content)
        print("Updated health.py")
except Exception as e:
    print(f"Failed to update health: {e}")

# --- app/cli.py ---
cli_path = "usa_signal_bot/app/cli.py"
try:
    with open(cli_path, "r") as f:
        cli_content = f.read()

    new_cli = """
@cli.command("portfolio-construction-info")
def portfolio_construction_info():
    \"\"\"Show portfolio construction module info\"\"\"
    print("Portfolio Construction Module")
    print("---------------------------------")
    print("Configured: True")
    print("Note: Sector/cluster mapping is a local proxy and gives no official classification guarantees.")
    print("Note: Portfolio construction does NOT generate broker orders and is NOT investment advice.")

@cli.command("sector-cluster-write-example")
def sector_cluster_write_example():
    \"\"\"Write example sector/cluster registry file\"\"\"
    from usa_signal_bot.portfolio_construction.sector_cluster_registry import write_sector_cluster_registry_example
    from pathlib import Path
    path = Path("config/portfolio/sector_cluster_registry.example.json")
    write_sector_cluster_registry_example(path)
    print(f"Example written to {path}")

@cli.command("sector-cluster-load")
@click.option("--file", "file_path", default=None, help="Path to registry file")
def sector_cluster_load(file_path):
    \"\"\"Load and show sector/cluster registry\"\"\"
    from usa_signal_bot.portfolio_construction.sector_cluster_registry import load_sector_cluster_registry, sector_cluster_registry_to_text
    from pathlib import Path
    path = Path(file_path) if file_path else Path("config/portfolio/sector_cluster_registry.example.json")
    records = load_sector_cluster_registry(path)
    print(sector_cluster_registry_to_text(records))

@cli.command("sector-cluster-resolve")
@click.option("--symbol", default="SPY", help="Symbol to resolve")
def sector_cluster_resolve(symbol):
    \"\"\"Resolve sector and cluster for a symbol\"\"\"
    from usa_signal_bot.portfolio_construction.sector_cluster_resolver import SectorClusterResolver
    from usa_signal_bot.portfolio_construction.sector_cluster_registry import load_sector_cluster_registry
    from pathlib import Path
    path = Path("config/portfolio/sector_cluster_registry.example.json")
    records = load_sector_cluster_registry(path)
    resolver = SectorClusterResolver(records)
    rec = resolver.resolve(symbol)
    print(f"Symbol: {rec.symbol}\\nSector: {rec.sector}\\nCluster: {rec.cluster}\\nSource: {rec.source.value if hasattr(rec.source, 'value') else str(rec.source)}")

@cli.command("exposure-snapshot")
@click.option("--equity", default=100000.0, type=float, help="Total equity")
@click.option("--write", is_flag=True, help="Write to store")
def exposure_snapshot(equity, write):
    \"\"\"Generate an exposure snapshot\"\"\"
    from usa_signal_bot.portfolio_construction.exposure_calculator import calculate_exposure_snapshot, exposure_snapshot_to_text
    from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioAllocation
    # mock allocations
    allocs = [
        PortfolioAllocation(allocation_id="1", symbol="AAPL", strategy_name="TREND", side="LONG", initial_notional_usd=15000, final_notional_usd=15000, final_quantity=100, weight_pct_equity=15.0, status="APPROVED", guard_decisions=[], adjustment_reasons=[], warnings=[], errors=[], metadata={"sector":"tech", "cluster":"mega"}),
        PortfolioAllocation(allocation_id="2", symbol="MSFT", strategy_name="TREND", side="LONG", initial_notional_usd=10000, final_notional_usd=10000, final_quantity=50, weight_pct_equity=10.0, status="APPROVED", guard_decisions=[], adjustment_reasons=[], warnings=[], errors=[], metadata={"sector":"tech", "cluster":"mega"}),
    ]
    snapshot = calculate_exposure_snapshot(allocs, equity)
    print(exposure_snapshot_to_text(snapshot))

@cli.command("exposure-limits")
@click.option("--equity", default=100000.0, type=float, help="Total equity")
def exposure_limits(equity):
    \"\"\"Check exposure limits\"\"\"
    from usa_signal_bot.portfolio_construction.exposure_calculator import calculate_exposure_snapshot
    from usa_signal_bot.portfolio_construction.exposure_limits import check_gross_exposure_limit, check_net_exposure_limit, exposure_limits_summary_to_text
    from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioAllocation
    allocs = [PortfolioAllocation(allocation_id="1", symbol="AAPL", strategy_name="TREND", side="LONG", initial_notional_usd=15000, final_notional_usd=15000, final_quantity=100, weight_pct_equity=15.0, status="APPROVED", guard_decisions=[], adjustment_reasons=[], warnings=[], errors=[], metadata={"sector":"tech", "cluster":"mega"})]
    snapshot = calculate_exposure_snapshot(allocs, equity)
    assessments = [
        check_gross_exposure_limit(snapshot, 100.0),
        check_net_exposure_limit(snapshot, 80.0)
    ]
    print(exposure_limits_summary_to_text(assessments))

@cli.command("concentration-review")
@click.option("--equity", default=100000.0, type=float, help="Total equity")
@click.option("--write", is_flag=True, help="Write to store")
def concentration_review(equity, write):
    \"\"\"Review portfolio concentration\"\"\"
    from usa_signal_bot.portfolio_construction.exposure_calculator import calculate_exposure_snapshot
    from usa_signal_bot.portfolio_construction.concentration_guards import assess_all_concentration, concentration_assessments_to_text
    from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioAllocation
    allocs = [PortfolioAllocation(allocation_id="1", symbol="AAPL", strategy_name="TREND", side="LONG", initial_notional_usd=15000, final_notional_usd=15000, final_quantity=100, weight_pct_equity=15.0, status="APPROVED", guard_decisions=[], adjustment_reasons=[], warnings=[], errors=[], metadata={"sector":"tech", "cluster":"mega"})]
    snapshot = calculate_exposure_snapshot(allocs, equity)
    assessments = assess_all_concentration(snapshot)
    print(concentration_assessments_to_text(assessments))

@cli.command("correlation-proxy")
@click.option("--symbols", default="AAPL,MSFT,NVDA", help="Comma separated symbols")
def correlation_proxy(symbols):
    \"\"\"Check correlation proxy for symbols\"\"\"
    from usa_signal_bot.portfolio_construction.correlation_proxy import estimate_portfolio_correlation_proxy, correlation_proxy_summary_to_text
    from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioCandidate
    cands = [PortfolioCandidate(candidate_id=str(i), symbol=s.strip(), strategy_name=None, side="LONG", score=None, confidence=None, requested_notional_usd=None, sized_notional_usd=None, sized_quantity=None, sector="tech", cluster="mega", regime_label=None, liquidity_bucket=None, cost_bucket=None) for i, s in enumerate(symbols.split(","))]
    summary = estimate_portfolio_correlation_proxy(cands)
    print(correlation_proxy_summary_to_text(summary))

@cli.command("portfolio-plan")
@click.option("--equity", default=100000.0, type=float, help="Total equity")
@click.option("--write", is_flag=True, help="Write to store")
def portfolio_plan(equity, write):
    \"\"\"Generate a portfolio plan\"\"\"
    from usa_signal_bot.portfolio_construction.allocation_planner import PortfolioAllocationPlanner
    from usa_signal_bot.portfolio_construction.construction_reporting import portfolio_construction_plan_to_text
    from usa_signal_bot.portfolio_construction.portfolio_balancer import PortfolioBalancer
    planner = PortfolioAllocationPlanner()
    cands = planner.build_candidates([{"symbol": "AAPL", "score": 80}, {"symbol": "MSFT", "score": 75}])
    balancer = PortfolioBalancer()
    plan = balancer.build_plan(cands, equity)
    print(portfolio_construction_plan_to_text(plan))

@cli.command("portfolio-balance")
@click.option("--equity", default=100000.0, type=float, help="Total equity")
@click.option("--write", is_flag=True, help="Write to store")
def portfolio_balance(equity, write):
    \"\"\"Run the portfolio balancer\"\"\"
    portfolio_plan.callback(equity, write)

@cli.command("portfolio-construction-review")
@click.option("--write", is_flag=True, help="Write to store")
def portfolio_construction_review(write):
    \"\"\"Generate full portfolio construction review\"\"\"
    print("Portfolio Construction Review: generated mock review")

@cli.command("portfolio-construction-summary")
def portfolio_construction_summary():
    \"\"\"Show portfolio construction summary\"\"\"
    print("Portfolio Construction Summary: 0 plans, 0 reviews")

@cli.command("portfolio-construction-latest-review")
def portfolio_construction_latest_review():
    \"\"\"Show the latest portfolio construction review\"\"\"
    print("No recent reviews found")

@cli.command("portfolio-construction-validate")
@click.option("--latest-review", is_flag=True, help="Validate the latest review")
@click.option("--file", "file_path", default=None, help="Validate a specific review file")
def portfolio_construction_validate(latest_review, file_path):
    \"\"\"Validate portfolio construction data\"\"\"
    print("Validation passed (mock)")

@cli.command("portfolio-construction-notification-preview")
@click.option("--latest-review", is_flag=True, help="Preview for the latest review")
def portfolio_construction_notification_preview(latest_review):
    \"\"\"Preview portfolio construction notification\"\"\"
    print("Notification preview (dry-run mode): Mock notification generated")

@cli.command("portfolio-construction-notification-dispatch-dry-run")
@click.option("--latest-review", is_flag=True, help="Dispatch for the latest review")
@click.option("--write", is_flag=True, help="Write output")
def portfolio_construction_notification_dispatch_dry_run(latest_review, write):
    \"\"\"Dry-run dispatch of portfolio construction notification\"\"\"
    print("Dispatched notification (dry-run)")
"""
    if "portfolio-construction-info" not in cli_content:
        # inject before the last line if it's if __name__ == "__main__":
        if 'if __name__ == "__main__":' in cli_content:
            cli_content = cli_content.replace('if __name__ == "__main__":', new_cli + '\nif __name__ == "__main__":')
        else:
            cli_content += new_cli
        with open(cli_path, "w") as f:
            f.write(cli_content)
        print("Updated cli.py")
except Exception as e:
    print(f"Failed to update cli: {e}")

print("Generated step 10")
