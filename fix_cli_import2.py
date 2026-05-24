from pathlib import Path
p = Path("usa_signal_bot/app/cli.py")
content = p.read_text()
# Find and fix the indentation error at the end of the file.
lines = content.split('\n')
fixed_lines = []
for line in lines:
    if line.strip() == '@cli.command("dry-admission-gate-info")':
        break # We removed the decorators but left the functions, causing indentation errors. Let's just remove everything we appended.
    fixed_lines.append(line)

p.write_text('\n'.join(fixed_lines))

# Now let's append it using argparse correctly.
to_add = """
def setup_dry_admission_gate_parsers(subparsers):
    p = subparsers.add_parser("dry-admission-gate-info", help="Dry Admission Gate Info")
    p = subparsers.add_parser("dry-admission-ingest-board-dossier")
    p.add_argument("--file", default=None)
    p = subparsers.add_parser("dry-admission-eligibility")
    p.add_argument("--write", action="store_true")
    p = subparsers.add_parser("shadow-replay-plan")
    p.add_argument("--write", action="store_true")
    p = subparsers.add_parser("shadow-replay-run")
    p.add_argument("--write", action="store_true")
    p = subparsers.add_parser("shadow-replay-analyze")
    p.add_argument("--write", action="store_true")
    p = subparsers.add_parser("board-evidence-freeze")
    p.add_argument("--write", action="store_true")
    p = subparsers.add_parser("board-evidence-freeze-validate")
    p.add_argument("--write", action="store_true")
    p = subparsers.add_parser("dry-admission-rules")
    p.add_argument("--write", action="store_true")
    p = subparsers.add_parser("dry-admission-assertions")
    p.add_argument("--write", action="store_true")
    p = subparsers.add_parser("final-dry-admission-gate")
    p.add_argument("--write", action="store_true")
    p = subparsers.add_parser("final-dry-admission-gate-validate")
    p.add_argument("--write", action="store_true")
    p = subparsers.add_parser("dry-admission-continuity")
    p.add_argument("--write", action="store_true")
    p = subparsers.add_parser("dry-admission-safety-check")
    p.add_argument("--write", action="store_true")
    p = subparsers.add_parser("dry-admission-audit")
    p.add_argument("--write", action="store_true")
    p = subparsers.add_parser("dry-admission-review")
    p.add_argument("--write", action="store_true")
    p = subparsers.add_parser("dry-admission-summary")
    p = subparsers.add_parser("dry-admission-latest-review")
    p = subparsers.add_parser("dry-admission-validate")
    p.add_argument("--latest-review", action="store_true")
    p.add_argument("--file", default=None)
    p = subparsers.add_parser("dry-admission-notification-preview")
    p.add_argument("--latest-review", action="store_true")
    p = subparsers.add_parser("dry-admission-notification-dispatch-dry-run")
    p.add_argument("--latest-review", action="store_true")
    p.add_argument("--write", action="store_true")
"""
p.write_text(p.read_text() + "\n" + to_add)
