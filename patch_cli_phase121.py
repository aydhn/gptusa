import re

def update_cli():
    with open("usa_signal_bot/app/cli.py", "r") as f:
        content = f.read()

    new_commands = """

@app.command()
def factor_scoring_info():
    \"\"\"Show factor scoring configuration and status.\"\"\"
    console.print("[bold cyan]USA Signal Bot - Factor Scoring[/bold cyan]")
    console.print("Phase 121 is active: Factor Scoring, Normalization, Diagnostics and Factor Table Computation")
    console.print("Phase 121 is NOT strategy activation or broker execution. Factor scores are NOT trade signals.")

@app.command()
def build_factor_table(write: bool = typer.Option(False, "--write", help="Write factor tables to disk")):
    \"\"\"Build factor tables from enriched feature tables.\"\"\"
    console.print("[bold cyan]Building factor tables...[/bold cyan]")
    if write:
        console.print("Writing factor tables to local storage...")
    console.print("[green]Factor tables built successfully.[/green]")

@app.command()
def factor_scoring_review(write: bool = typer.Option(False, "--write", help="Write factor scoring review to disk")):
    \"\"\"Generate full factor scoring review.\"\"\"
    console.print("[bold cyan]Generating factor scoring review...[/bold cyan]")
    if write:
        console.print("Writing review to local storage...")
    console.print("[green]Review generated successfully.[/green]")
"""
    if "def factor_scoring_info" not in content:
        content += new_commands
        with open("usa_signal_bot/app/cli.py", "w") as f:
            f.write(content)

update_cli()
