import os
import re

# Since `click` isn't in requirements.txt, we must revert the test_cli.py updates that use it.
# We will use subprocess instead, like the original test_cli.py does.

with open("tests/test_cli.py", "r") as f:
    content = f.read()

# Filter out the CliRunner tests and imports
lines = content.split('\n')
new_lines = []
skip = False
for line in lines:
    if "from click.testing import CliRunner" in line or "from usa_signal_bot.app.cli import cli" in line:
        continue
    if "def test_cost_robustness_info():" in line or "def test_cost_stress_scenarios():" in line or "def test_slippage_stress():" in line or "def test_spread_stress():" in line or "def test_impact_stress():" in line or "def test_fee_stress():" in line or "def test_participation_stress():" in line or "def test_fill_realism_stress():" in line or "def test_sensitivity_matrix():" in line or "def test_walk_forward_cost_robustness():" in line or "def test_cost_fragility():" in line or "def test_breakeven_costs():" in line or "def test_cost_robustness_review():" in line or "def test_cost_robustness_summary():" in line:
        skip = True
        continue
    if skip and (line.startswith("def ") or line.strip() == ""):
        # if we hit a new def or blank line after skipping, we might stop skipping if it's not a cli test.
        # But actually let's just rewrite the specific tests we added.
        pass
    if not skip:
        new_lines.append(line)
    if skip and line.strip() == "" and len(new_lines)>0 and new_lines[-1] != "":
        skip = False # Reset skip on blank line if appropriate, actually let's be more precise.

# Better: Just recreate the file with the subprocess approach
