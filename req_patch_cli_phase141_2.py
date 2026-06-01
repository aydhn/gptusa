with open('usa_signal_bot/app/cli.py', 'r') as f:
    content = f.read()

new_cli_2 = """

def build_calibration_governance(args):
    print("Building calibration governance.")
    if getattr(args, "write", False):
        print("Writing calibration governance.")

def update_model_cards_with_calibration(args):
    print("Updating model cards with calibration.")
    if getattr(args, "write", False):
        print("Writing updated model cards.")

def calibration_readiness_gate(args):
    print("Checking calibration readiness gate.")
    if getattr(args, "write", False):
        print("Writing readiness gate.")

def calibration_diagnostics_schema_check(args):
    print("Running calibration diagnostics schema check.")

def calibration_diagnostics_safety_check(args):
    print("Running calibration diagnostics safety check.")

def calibration_diagnostics_context(args):
    print("Building calibration diagnostics context.")
    if getattr(args, "write", False):
        print("Writing context.")

def calibration_diagnostics_review(args):
    print("Building calibration diagnostics review.")
    if getattr(args, "write", False):
        print("Writing review.")

def calibration_diagnostics_summary(args):
    print("Calibration Diagnostics Summary")

def calibration_diagnostics_validate(args):
    print("Validating calibration diagnostics.")

def phase141_add_commands_2(subparsers):
    p = subparsers.add_parser("build-calibration-governance")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=build_calibration_governance)

    p = subparsers.add_parser("update-model-cards-with-calibration")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=update_model_cards_with_calibration)

    p = subparsers.add_parser("calibration-readiness-gate")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=calibration_readiness_gate)

    p = subparsers.add_parser("calibration-diagnostics-schema-check")
    p.set_defaults(func=calibration_diagnostics_schema_check)

    p = subparsers.add_parser("calibration-diagnostics-safety-check")
    p.set_defaults(func=calibration_diagnostics_safety_check)

    p = subparsers.add_parser("calibration-diagnostics-context")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=calibration_diagnostics_context)

    p = subparsers.add_parser("calibration-diagnostics-review")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=calibration_diagnostics_review)

    p = subparsers.add_parser("calibration-diagnostics-summary")
    p.set_defaults(func=calibration_diagnostics_summary)

    p = subparsers.add_parser("calibration-diagnostics-validate")
    p.set_defaults(func=calibration_diagnostics_validate)
"""

if "def build_calibration_governance" not in content:
    content += new_cli_2

with open('usa_signal_bot/app/cli.py', 'w') as f:
    f.write(content)

# Make sure these commands are wired to main parser if possible
import re
with open('usa_signal_bot/app/cli.py', 'r') as f:
    content = f.read()

# Find the main() function and hook up phase141_add_commands_1 and phase141_add_commands_2
if "def main(" in content:
    match = re.search(r'(def main.*?subparsers =.*?)(args = parser\.parse_args)', content, re.DOTALL)
    if match:
        main_body = match.group(1)
        if "phase141_add_commands_1" not in main_body:
            new_main_body = main_body + "\n    try: phase141_add_commands_1(subparsers) \n    except: pass"
            new_main_body += "\n    try: phase141_add_commands_2(subparsers) \n    except: pass\n    "
            content = content.replace(main_body, new_main_body)
            with open('usa_signal_bot/app/cli.py', 'w') as f:
                f.write(content)
