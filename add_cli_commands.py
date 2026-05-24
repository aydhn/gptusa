import re
from pathlib import Path

def update_cli():
    path = Path("usa_signal_bot/app/cli.py")
    if not path.exists():
        return
    content = path.read_text()

    if "dry_admission_gate_info" not in content:
        cli_commands = """
@cli.command("dry-admission-gate-info")
def dry_admission_gate_info():
    print("Dry Admission Gate Info")
    print("Shadow replay / board evidence freeze / final dry-admission gate are metadata-only. Not an activation.")

@cli.command("dry-admission-ingest-board-dossier")
@click.option("--file", default=None)
def dry_admission_ingest_board_dossier(file):
    print("dry_admission_ingest_board_dossier")

@cli.command("dry-admission-eligibility")
@click.option("--write", is_flag=True)
def dry_admission_eligibility(write):
    print("dry_admission_eligibility")

@cli.command("shadow-replay-plan")
@click.option("--write", is_flag=True)
def shadow_replay_plan(write):
    print("shadow_replay_plan")

@cli.command("shadow-replay-run")
@click.option("--write", is_flag=True)
def shadow_replay_run(write):
    print("shadow_replay_run")

@cli.command("shadow-replay-analyze")
@click.option("--write", is_flag=True)
def shadow_replay_analyze(write):
    print("shadow_replay_analyze")

@cli.command("board-evidence-freeze")
@click.option("--write", is_flag=True)
def board_evidence_freeze(write):
    print("board_evidence_freeze")

@cli.command("board-evidence-freeze-validate")
@click.option("--write", is_flag=True)
def board_evidence_freeze_validate(write):
    print("board_evidence_freeze_validate")

@cli.command("dry-admission-rules")
@click.option("--write", is_flag=True)
def dry_admission_rules(write):
    print("dry_admission_rules")

@cli.command("dry-admission-assertions")
@click.option("--write", is_flag=True)
def dry_admission_assertions(write):
    print("dry_admission_assertions")

@cli.command("final-dry-admission-gate")
@click.option("--write", is_flag=True)
def final_dry_admission_gate(write):
    print("final_dry_admission_gate")

@cli.command("final-dry-admission-gate-validate")
@click.option("--write", is_flag=True)
def final_dry_admission_gate_validate(write):
    print("final_dry_admission_gate_validate")

@cli.command("dry-admission-continuity")
@click.option("--write", is_flag=True)
def dry_admission_continuity(write):
    print("dry_admission_continuity")

@cli.command("dry-admission-safety-check")
@click.option("--write", is_flag=True)
def dry_admission_safety_check(write):
    print("dry_admission_safety_check")

@cli.command("dry-admission-audit")
@click.option("--write", is_flag=True)
def dry_admission_audit(write):
    print("dry_admission_audit")

@cli.command("dry-admission-review")
@click.option("--write", is_flag=True)
def dry_admission_review(write):
    print("dry_admission_review")

@cli.command("dry-admission-summary")
def dry_admission_summary():
    print("dry_admission_summary")

@cli.command("dry-admission-latest-review")
def dry_admission_latest_review():
    print("dry_admission_latest_review")

@cli.command("dry-admission-validate")
@click.option("--latest-review", is_flag=True)
@click.option("--file", default=None)
def dry_admission_validate(latest_review, file):
    print("dry_admission_validate")

@cli.command("dry-admission-notification-preview")
@click.option("--latest-review", is_flag=True)
def dry_admission_notification_preview(latest_review):
    print("dry_admission_notification_preview")

@cli.command("dry-admission-notification-dispatch-dry-run")
@click.option("--latest-review", is_flag=True)
@click.option("--write", is_flag=True)
def dry_admission_notification_dispatch_dry_run(latest_review, write):
    print("dry_admission_notification_dispatch_dry_run")
"""
        content += cli_commands
        path.write_text(content)

update_cli()
