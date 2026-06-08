import typer
from pathlib import Path
from usa_signal_bot.portfolio.construction.portfolio_construction_report import build_portfolio_construction_context, build_portfolio_construction_full_review, portfolio_construction_limitations_text
from usa_signal_bot.portfolio.construction.portfolio_construction_policy import build_default_portfolio_construction_policy
from usa_signal_bot.portfolio.construction.sandbox_allocation_method_contracts import build_sandbox_allocation_method_contracts
from usa_signal_bot.portfolio.construction.equal_sandbox_allocation import build_equal_sandbox_allocation
from usa_signal_bot.portfolio.construction.prototype_exposure_table import build_prototype_exposure_table
from usa_signal_bot.portfolio.construction.allocation_sandbox_safety_boundary import build_allocation_sandbox_safety_boundary_rules, build_allocation_sandbox_safety_boundary_result
from usa_signal_bot.portfolio.construction.phase156_readiness_gate import build_phase156_readiness_gate
from usa_signal_bot.portfolio.construction.allocation_sandbox_comparison_report import build_allocation_sandbox_comparison_report
from usa_signal_bot.portfolio.construction.portfolio_construction_validation_report import build_portfolio_construction_validation_report

app = typer.Typer(help="Phase 155 Portfolio Construction Sandbox Commands")

@app.command("portfolio-construction-info")
def portfolio_construction_info():
    """Print info about Phase 155"""
    typer.echo("Phase 155 Portfolio Construction Prototype & Allocation Sandbox")
    typer.echo(portfolio_construction_limitations_text())

@app.command("build-portfolio-construction-policy")
def build_policy(write: bool = False):
    """Build and preview a default sandbox policy"""
    policy = build_default_portfolio_construction_policy()
    typer.echo(f"Policy Built: {policy.policy_name}")
    typer.echo(f"Max Sandbox Weight: {policy.max_sandbox_weight_fraction}")

@app.command("build-equal-sandbox-allocation")
def build_equal_sandbox(write: bool = False):
    """Build equal sandbox allocation using default policy"""
    policy = build_default_portfolio_construction_policy()
    results = build_equal_sandbox_allocation([], policy)
    typer.echo(f"Built equal allocation with {len(results)} records.")

@app.command("build-prototype-exposure-table")
def build_exposure_table(write: bool = False):
    """Build prototype exposure table"""
    table = build_prototype_exposure_table([], [])
    typer.echo(f"Built exposure table with hash: {table.table_hash}")

@app.command("portfolio-construction-review")
def portfolio_review(write: bool = False):
    """Run full portfolio construction review"""
    context = build_portfolio_construction_context()
    policy = build_default_portfolio_construction_policy()
    contracts = build_sandbox_allocation_method_contracts(policy)
    table = build_prototype_exposure_table([], [])
    comp = build_allocation_sandbox_comparison_report([], table, [])
    val = build_portfolio_construction_validation_report(policy, contracts, comp)
    rules = build_allocation_sandbox_safety_boundary_rules()
    bound = build_allocation_sandbox_safety_boundary_result(rules)
    gate = build_phase156_readiness_gate(policy, contracts, comp, val, bound)

    context.policy = policy
    context.method_contracts = contracts
    context.exposure_table = table
    context.comparison_report = comp
    context.validation_report = val
    context.safety_boundary = bound
    context.phase156_readiness_gate = gate

    review = build_portfolio_construction_full_review(context)
    typer.echo(f"Review ID: {review.review_id}")
    typer.echo(f"Safety Passed: {bound.boundary_passed}")
    typer.echo(f"Ready for Phase 156: {gate.ready_for_phase156}")

if __name__ == "__main__":
    app()
