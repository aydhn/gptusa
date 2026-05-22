import subprocess
import sys

def run_cmd(args):
    cmd = [sys.executable, "-m", "usa_signal_bot", *args]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res

def test_cli_commands():
    commands = [
        ["--final-handoff-info"],
        ["--final-handoff-ingest-readiness"],
        ["--handoff-registry-ingest"],
        ["--final-handoff-eligibility"],
        ["--final-handoff-review"],
        ["--sealed-archive-manifest"],
        ["--sealed-archive-seal"],
        ["--sealed-archive-integrity"],
        ["--pre-paper-checkpoint-gates"],
        ["--pre-paper-checkpoint-decision"],
        ["--final-handoff-non-execution-compliance"],
        ["--final-handoff-safety-check"],
        ["--final-handoff-audit"],
        ["--final-handoff-full-review"],
        ["--final-handoff-summary"],
        ["--final-handoff-latest-review"],
        ["--final-handoff-validate"],
        ["--final-handoff-notification-preview"],
        ["--final-handoff-notification-dispatch-dry-run"]
    ]
    for cmd in commands:
        res = run_cmd(cmd)
        assert res.returncode == 0, f"Command {cmd} failed with {res.returncode}. stderr: {res.stderr}"

if __name__ == "__main__":
    test_cli_commands()
    print("All CLI tests passed!")
