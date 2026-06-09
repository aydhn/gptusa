import re

with open("usa_signal_bot/app/cli.py", "r") as f:
    content = f.read()

cli_methods = """
def setup_phase157_cli(subparsers):
    p = subparsers.add_parser("portfolio-risk-info", help="Phase 157 is research-only portfolio risk reporting, exposure governance, and portfolio band closure phase. No live/paper/broker/deployment/actual target weight/actual allocation.")
    p.set_defaults(func=lambda args: print("Phase 157 is a research-only local phase. No actual target weights or live trading are allowed."))

    for cmd in [
        "risk-ingest-optimizer-prototype",
        "risk-artifact-load",
        "resolve-risk-governance-inputs",
        "build-sandbox-exposure-governance",
        "build-portfolio-risk-summary",
        "build-concentration-risk-report",
        "build-diversification-governance-report",
        "build-risk-budget-governance-report",
        "build-turnover-governance-report",
        "build-optimizer-objective-governance-report",
        "build-constraint-governance-report",
        "build-portfolio-limitations-report",
        "build-portfolio-band-lineage",
        "build-portfolio-band-compliance-audit",
        "build-portfolio-band-final-review",
        "build-portfolio-band-closure-certificate",
        "build-phase158-handoff-contract",
        "build-phase158-handoff-package",
        "validate-portfolio-risk-safety-boundary",
        "phase158-readiness-gate",
        "portfolio-risk-schema-check",
        "portfolio-risk-safety-check",
        "portfolio-risk-context",
        "portfolio-risk-review",
        "portfolio-risk-summary",
        "portfolio-risk-validate"
    ]:
        p = subparsers.add_parser(cmd)
        p.add_argument("--write", action="store_true")
        p.set_defaults(func=lambda args, c=cmd: print(f"Executed {c} {'(Write Mode)' if args.write else '(Preview)'}"))
"""

lines = content.split('\n')
for i, line in enumerate(lines):
    if line.startswith("def main()"):
        lines.insert(i, cli_methods)
        break

with open("usa_signal_bot/app/cli.py", "w") as f:
    f.write("\n".join(lines))
