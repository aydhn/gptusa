import subprocess

def test_cli_commands():
    commands = [
        ["python", "-m", "usa_signal_bot.app.cli", "paper-shadow-info"],
        ["python", "-m", "usa_signal_bot.app.cli", "shadow-ingest-sandbox"],
        ["python", "-m", "usa_signal_bot.app.cli", "shadow-context", "--equity", "100000"],
        ["python", "-m", "usa_signal_bot.app.cli", "shadow-portfolio-init", "--equity", "100000"],
        ["python", "-m", "usa_signal_bot.app.cli", "shadow-signal-rehearsal"],
        ["python", "-m", "usa_signal_bot.app.cli", "shadow-candidate-selection", "--min-score", "50"],
        ["python", "-m", "usa_signal_bot.app.cli", "shadow-order-intents", "--notional", "1000"],
        ["python", "-m", "usa_signal_bot.app.cli", "shadow-risk-gate"],
        ["python", "-m", "usa_signal_bot.app.cli", "shadow-fill-simulate"],
        ["python", "-m", "usa_signal_bot.app.cli", "shadow-ledger"],
        ["python", "-m", "usa_signal_bot.app.cli", "shadow-pnl", "--equity", "100000"],
        ["python", "-m", "usa_signal_bot.app.cli", "shadow-rebalance"],
        ["python", "-m", "usa_signal_bot.app.cli", "shadow-notification-preview"],
        ["python", "-m", "usa_signal_bot.app.cli", "shadow-safety-check"],
        ["python", "-m", "usa_signal_bot.app.cli", "shadow-session-run", "--runtime-mode", "full_paper_shadow", "--equity", "100000"],
        ["python", "-m", "usa_signal_bot.app.cli", "shadow-session-registry"],
        ["python", "-m", "usa_signal_bot.app.cli", "shadow-result-analyze"],
        ["python", "-m", "usa_signal_bot.app.cli", "paper-shadow-review"],
        ["python", "-m", "usa_signal_bot.app.cli", "paper-shadow-summary"],
        ["python", "-m", "usa_signal_bot.app.cli", "paper-shadow-latest-review"],
        ["python", "-m", "usa_signal_bot.app.cli", "paper-shadow-validate"],
        ["python", "-m", "usa_signal_bot.app.cli", "paper-shadow-notification-preview"],
        ["python", "-m", "usa_signal_bot.app.cli", "paper-shadow-notification-dispatch-dry-run"],
    ]

    for cmd in commands:
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command {' '.join(cmd)} failed with output: {result.stderr}"

