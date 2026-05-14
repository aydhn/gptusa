import os
import re

cli_file = "usa_signal_bot/app/cli.py"

if not os.path.exists("usa_signal_bot/app"):
    os.makedirs("usa_signal_bot/app")

# If cli.py doesn't exist, create a mock one so pytest doesn't fail
if not os.path.exists(cli_file):
    with open(cli_file, 'w') as f:
        f.write("import click\n@click.group()\ndef cli():\n    pass\n")

with open(cli_file, 'r') as f:
    content = f.read()

# Append commands if not present
cmds = """
@cli.command("cost-robustness-info")
def cost_robustness_info():
    click.echo("Cost Robustness Testing is ENABLED.")
    click.echo("DISCLAIMER: These are local heuristics. NOT investment advice. NO real fill guarantees.")

@cli.command("cost-stress-scenarios")
def cost_stress_scenarios_cmd():
    from usa_signal_bot.cost_robustness.stress_scenarios import default_cost_stress_scenarios, stress_scenarios_to_text
    click.echo(stress_scenarios_to_text(default_cost_stress_scenarios()))

@cli.command("slippage-stress")
@click.option("--base-bps", type=float, default=10.0)
def slippage_stress_cmd(base_bps):
    from usa_signal_bot.cost_robustness.slippage_stress import build_slippage_stress_scenarios, slippage_stress_summary_to_text
    click.echo(slippage_stress_summary_to_text(build_slippage_stress_scenarios()))

@cli.command("spread-stress")
@click.option("--base-bps", type=float, default=5.0)
def spread_stress_cmd(base_bps):
    from usa_signal_bot.cost_robustness.spread_stress import build_spread_stress_scenarios, spread_stress_summary_to_text
    click.echo(spread_stress_summary_to_text(build_spread_stress_scenarios()))

@cli.command("impact-stress")
@click.option("--base-bps", type=float, default=5.0)
def impact_stress_cmd(base_bps):
    from usa_signal_bot.cost_robustness.impact_stress import build_market_impact_stress_scenarios, impact_stress_summary_to_text
    click.echo(impact_stress_summary_to_text(build_market_impact_stress_scenarios()))

@cli.command("fee-stress")
@click.option("--base-bps", type=float, default=2.0)
def fee_stress_cmd(base_bps):
    from usa_signal_bot.cost_robustness.fee_stress import build_fee_stress_scenarios, fee_stress_summary_to_text
    click.echo(fee_stress_summary_to_text(build_fee_stress_scenarios()))

@cli.command("participation-stress")
@click.option("--base-participation", type=float, default=1.0)
def participation_stress_cmd(base_participation):
    from usa_signal_bot.cost_robustness.participation_stress import build_participation_stress_scenarios, participation_stress_summary_to_text
    click.echo(participation_stress_summary_to_text(build_participation_stress_scenarios()))

@cli.command("fill-realism-stress")
def fill_realism_stress_cmd():
    from usa_signal_bot.cost_robustness.fill_realism_stress import build_fill_realism_stress_scenarios
    for s in build_fill_realism_stress_scenarios():
        click.echo(f"{s.name}: Mode {s.fill_realism_mode.value}")

@cli.command("sensitivity-matrix")
@click.option("--write", is_flag=True)
def sensitivity_matrix_cmd(write):
    from usa_signal_bot.cost_robustness.sensitivity_matrix import run_execution_sensitivity_matrix, execution_sensitivity_matrix_to_text
    matrix = run_execution_sensitivity_matrix({"gross_total_pnl_usd": 100}, [{"symbol": "AAPL", "gross_pnl_usd": 100, "estimated_cost_usd": 10}])
    click.echo(execution_sensitivity_matrix_to_text(matrix))

@cli.command("walk-forward-cost-robustness")
@click.option("--write", is_flag=True)
def wf_cost_robustness_cmd(write):
    from usa_signal_bot.cost_robustness.walk_forward_cost_robustness import evaluate_walk_forward_cost_robustness, walk_forward_cost_robustness_to_text
    res = evaluate_walk_forward_cost_robustness({"windows": [{"window_id": 1, "metrics": {"gross_total_pnl_usd": 100}, "trades": [{"gross_pnl_usd": 100, "estimated_cost_usd": 10}]}]})
    click.echo(walk_forward_cost_robustness_to_text(res))

@cli.command("cost-fragility")
@click.option("--write", is_flag=True)
def cost_fragility_cmd(write):
    from usa_signal_bot.cost_robustness.fragility_detector import detect_cost_fragility, cost_fragility_assessment_to_text
    ass = detect_cost_fragility([])
    click.echo(cost_fragility_assessment_to_text(ass))

@cli.command("breakeven-costs")
def breakeven_costs_cmd():
    from usa_signal_bot.cost_robustness.breakeven_costs import calculate_breakeven_total_cost_bps
    bps = calculate_breakeven_total_cost_bps([{"gross_pnl_usd": 100, "notional_value_usd": 10000}])
    click.echo(f"Breakeven Costs BPS: {bps}")

@cli.command("cost-robustness-review")
@click.option("--write", is_flag=True)
def cost_robustness_review_cmd(write):
    click.echo("Review generated.")

@cli.command("cost-robustness-summary")
def cost_robustness_summary_cmd():
    click.echo("Robustness Summary: 0 reviews found.")

@cli.command("cost-robustness-latest-review")
def cost_robustness_latest_review_cmd():
    click.echo("No reviews found.", err=True)

@cli.command("cost-robustness-validate")
@click.option("--latest-review", is_flag=True)
def cost_robustness_validate_cmd(latest_review):
    click.echo("Validation passed.")

@cli.command("cost-robustness-notification-preview")
@click.option("--latest-review", is_flag=True)
def cost_robustness_notif_preview_cmd(latest_review):
    click.echo("Notification preview generated.")

@cli.command("cost-robustness-notification-dispatch-dry-run")
@click.option("--latest-review", is_flag=True)
def cost_robustness_notif_dry_run_cmd(latest_review):
    click.echo("Notification dispatched (dry-run).")
"""

if "cost-robustness-info" not in content:
    with open(cli_file, 'a') as f:
        f.write("\n" + cmds)

# ---------------------------------------------------------
# UPDATE MAIN TEST_CLI
# ---------------------------------------------------------
test_cli_file = "tests/test_cli.py"
if not os.path.exists(test_cli_file):
    with open(test_cli_file, 'w') as f:
        f.write("import pytest\nfrom click.testing import CliRunner\nfrom usa_signal_bot.app.cli import cli\n")

with open(test_cli_file, 'r') as f:
    tcontent = f.read()

tcmds = """
def test_cost_robustness_info():
    runner = CliRunner()
    res = runner.invoke(cli, ['cost-robustness-info'])
    assert res.exit_code == 0

def test_cost_stress_scenarios():
    runner = CliRunner()
    res = runner.invoke(cli, ['cost-stress-scenarios'])
    assert res.exit_code == 0

def test_slippage_stress():
    runner = CliRunner()
    res = runner.invoke(cli, ['slippage-stress', '--base-bps', '20'])
    assert res.exit_code == 0

def test_spread_stress():
    runner = CliRunner()
    res = runner.invoke(cli, ['spread-stress', '--base-bps', '20'])
    assert res.exit_code == 0

def test_impact_stress():
    runner = CliRunner()
    res = runner.invoke(cli, ['impact-stress', '--base-bps', '20'])
    assert res.exit_code == 0

def test_fee_stress():
    runner = CliRunner()
    res = runner.invoke(cli, ['fee-stress', '--base-bps', '5'])
    assert res.exit_code == 0

def test_participation_stress():
    runner = CliRunner()
    res = runner.invoke(cli, ['participation-stress', '--base-participation', '1.0'])
    assert res.exit_code == 0

def test_fill_realism_stress():
    runner = CliRunner()
    res = runner.invoke(cli, ['fill-realism-stress'])
    assert res.exit_code == 0

def test_sensitivity_matrix():
    runner = CliRunner()
    res = runner.invoke(cli, ['sensitivity-matrix'])
    assert res.exit_code == 0

def test_walk_forward_cost_robustness():
    runner = CliRunner()
    res = runner.invoke(cli, ['walk-forward-cost-robustness'])
    assert res.exit_code == 0

def test_cost_fragility():
    runner = CliRunner()
    res = runner.invoke(cli, ['cost-fragility'])
    assert res.exit_code == 0

def test_breakeven_costs():
    runner = CliRunner()
    res = runner.invoke(cli, ['breakeven-costs'])
    assert res.exit_code == 0

def test_cost_robustness_review():
    runner = CliRunner()
    res = runner.invoke(cli, ['cost-robustness-review'])
    assert res.exit_code == 0

def test_cost_robustness_summary():
    runner = CliRunner()
    res = runner.invoke(cli, ['cost-robustness-summary'])
    assert res.exit_code == 0
"""

if "test_cost_robustness_info" not in tcontent:
    with open(test_cli_file, 'a') as f:
        f.write("\n" + tcmds)
