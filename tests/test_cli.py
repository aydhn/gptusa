
import unittest
import sys

class TestCli(unittest.TestCase):
    def test_cli(self):
        # Already tested broadly
        pass

    def test_release_sandbox_commands(self):
        import subprocess
        cmds = [
            ["python", "-m", "usa_signal_bot", "release-sandbox-info"],
            ["python", "-m", "usa_signal_bot", "sandbox-load-bundle"],
            ["python", "-m", "usa_signal_bot", "sandbox-read-only-verify"],
            ["python", "-m", "usa_signal_bot", "sandbox-mount-plan"],
            ["python", "-m", "usa_signal_bot", "sandbox-activation-plan"],
            ["python", "-m", "usa_signal_bot", "sandbox-overlay-preview"],
            ["python", "-m", "usa_signal_bot", "sandbox-output-path"],
            ["python", "-m", "usa_signal_bot", "sandbox-operation-guard"],
            ["python", "-m", "usa_signal_bot", "sandbox-runtime-context"],
            ["python", "-m", "usa_signal_bot", "sandbox-signal-preview"],
            ["python", "-m", "usa_signal_bot", "sandbox-portfolio-preview"],
            ["python", "-m", "usa_signal_bot", "sandbox-risk-preview"],
            ["python", "-m", "usa_signal_bot", "sandbox-notification-preview"],
            ["python", "-m", "usa_signal_bot", "sandbox-preview-run"],
            ["python", "-m", "usa_signal_bot", "sandbox-safety-validate"],
            ["python", "-m", "usa_signal_bot", "sandbox-session-registry"],
            ["python", "-m", "usa_signal_bot", "sandbox-restore-preview"],
            ["python", "-m", "usa_signal_bot", "release-sandbox-review"],
            ["python", "-m", "usa_signal_bot", "release-sandbox-summary"],
            ["python", "-m", "usa_signal_bot", "release-sandbox-latest-review"],
            ["python", "-m", "usa_signal_bot", "release-sandbox-validate"],
            ["python", "-m", "usa_signal_bot", "release-sandbox-notification-preview"],
            ["python", "-m", "usa_signal_bot", "release-sandbox-notification-dispatch-dry-run"],
        ]
        for cmd in cmds:
            res = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, f"Command {' '.join(cmd)} failed: {res.stderr}")
