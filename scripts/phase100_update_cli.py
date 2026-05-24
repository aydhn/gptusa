import re

def update_cli():
    with open('usa_signal_bot/app/cli.py', 'r') as f:
        content = f.read()

    cli_parsers = """
def setup_pre_paper_handoff_freeze_gate_parsers(subparsers):
    cmd = subparsers.add_parser("handoff-freeze-info", help="Show handoff freeze info")

    cmd = subparsers.add_parser("handoff-freeze-ingest-simulator-dossier", help="Ingest simulator dossier")
    cmd.add_argument("--file", type=str, help="Path to json file")

    cmd = subparsers.add_parser("handoff-freeze-eligibility", help="Check handoff freeze eligibility")
    cmd.add_argument("--write", action="store_true", help="Write result")

    cmd = subparsers.add_parser("sandbox-replay-plan", help="Build sandbox replay plan")
    cmd.add_argument("--write", action="store_true", help="Write result")

    cmd = subparsers.add_parser("sandbox-replay-run", help="Run sandbox replay")
    cmd.add_argument("--write", action="store_true", help="Write result")

    cmd = subparsers.add_parser("sandbox-replay-analyze", help="Analyze sandbox replay")
    cmd.add_argument("--write", action="store_true", help="Write result")

    cmd = subparsers.add_parser("simulator-evidence-freeze", help="Build simulator evidence freeze")
    cmd.add_argument("--write", action="store_true", help="Write result")

    cmd = subparsers.add_parser("simulator-evidence-freeze-validate", help="Validate simulator evidence freeze")
    cmd.add_argument("--write", action="store_true", help="Write result")

    cmd = subparsers.add_parser("handoff-freeze-rules", help="Build handoff freeze rules")
    cmd.add_argument("--write", action="store_true", help="Write result")

    cmd = subparsers.add_parser("handoff-freeze-assertions", help="Build handoff freeze assertions")
    cmd.add_argument("--write", action="store_true", help="Write result")

    cmd = subparsers.add_parser("final-handoff-freeze-gate", help="Build final handoff freeze gate")
    cmd.add_argument("--write", action="store_true", help="Write result")

    cmd = subparsers.add_parser("final-handoff-freeze-gate-validate", help="Validate final handoff freeze gate")
    cmd.add_argument("--write", action="store_true", help="Write result")

    cmd = subparsers.add_parser("handoff-freeze-continuity", help="Check handoff freeze continuity")
    cmd.add_argument("--write", action="store_true", help="Write result")

    cmd = subparsers.add_parser("handoff-freeze-safety-check", help="Check handoff freeze safety")
    cmd.add_argument("--write", action="store_true", help="Write result")

    cmd = subparsers.add_parser("handoff-freeze-audit", help="Build handoff freeze audit")
    cmd.add_argument("--write", action="store_true", help="Write result")

    cmd = subparsers.add_parser("handoff-freeze-review", help="Build handoff freeze full review")
    cmd.add_argument("--write", action="store_true", help="Write result")

    cmd = subparsers.add_parser("handoff-freeze-summary", help="Show handoff freeze store summary")

    cmd = subparsers.add_parser("handoff-freeze-latest-review", help="Show latest handoff freeze full review")

    cmd = subparsers.add_parser("handoff-freeze-validate", help="Validate handoff freeze report")
    cmd.add_argument("--latest-review", action="store_true", help="Use latest review")
    cmd.add_argument("--file", type=str, help="Path to json file")

    cmd = subparsers.add_parser("handoff-freeze-notification-preview", help="Preview handoff freeze notification")
    cmd.add_argument("--latest-review", action="store_true", help="Use latest review")

    cmd = subparsers.add_parser("handoff-freeze-notification-dispatch-dry-run", help="Dry run handoff freeze notification")
    cmd.add_argument("--latest-review", action="store_true", help="Use latest review")
    cmd.add_argument("--write", action="store_true", help="Write result")
"""

    if "setup_pre_paper_handoff_freeze_gate_parsers" not in content:
        content += cli_parsers

        main_func_patch = """
    setup_pre_paper_handoff_freeze_gate_parsers(subparsers)
"""
        content = re.sub(
            r'(def main\(\):.*?)(?=args = parser\.parse_args\(\))',
            r'\1' + main_func_patch + '\n    ',
            content,
            flags=re.MULTILINE | re.DOTALL
        )

        with open('usa_signal_bot/app/cli.py', 'w') as f:
            f.write(content)
        print("CLI updated.")

if __name__ == '__main__':
    update_cli()
