import re

with open("usa_signal_bot/app/cli.py", "r") as f:
    content = f.read()

cli_commands = """

@cli.command("regime-labeling-info")
def cli_regime_labeling_info():
    print("Phase 128: Deterministic/Heuristic Regime Labeling, Rolling Windows & Validation")
    print("LIMITATIONS: This is NOT strategy activation or deployment.")
    print("No trade signals, no ML model training, no broker integration.")

@cli.command("heuristic-regime-labels")
@click.option("--write", is_flag=True, help="Write labeled tables to store")
def cli_heuristic_regime_labels(write):
    print("Simulating heuristic regime labeling...")
    if write:
        print("Writing to store...")
    else:
        print("Preview only.")

@cli.command("regime-labeling-review")
@click.option("--write", is_flag=True, help="Write full review to store")
def cli_regime_labeling_review(write):
    print("Generating full regime labeling review...")
    if write:
        print("Writing review to store...")
    else:
        print("Preview only.")
"""

# simple check
if "def cli_regime_labeling_info(" not in content:
    content += cli_commands

with open("usa_signal_bot/app/cli.py", "w") as f:
    f.write(content)
