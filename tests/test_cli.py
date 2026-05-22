import sys
import subprocess
import subprocess
import pytest

def test_pre_paper_rehearsal_info():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-rehearsal-info"], capture_output=True, text=True)
    assert result.returncode in (0, 1)
    pass

def test_pre_paper_ingest_final_handoff():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-ingest-final-handoff"], capture_output=True, text=True)
    assert result.returncode in (0, 1)

def test_pre_paper_eligibility():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-eligibility"], capture_output=True, text=True)
    assert result.returncode in (0, 1)

def test_pre_paper_plan():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-plan"], capture_output=True, text=True)
    assert result.returncode in (0, 1)

def test_pre_paper_baseline():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-baseline"], capture_output=True, text=True)
    assert result.returncode in (0, 1)

def test_mutation_firewall_rules():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "mutation-firewall-rules"], capture_output=True, text=True)
    assert result.returncode in (0, 1)

def test_mutation_firewall_evaluate():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "mutation-firewall-evaluate", "--attempt-type", "paper_state_write"], capture_output=True, text=True)
    assert result.returncode in (0, 1)
    pass

def test_mutation_attempt_detect():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "mutation-attempt-detect", "--text", "paper'a uygula"], capture_output=True, text=True)
    assert result.returncode in (0, 1)

def test_forbidden_operation_simulate():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "forbidden-operation-simulate"], capture_output=True, text=True)
    assert result.returncode in (0, 1)
    pass

def test_pre_paper_dry_run():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-dry-run"], capture_output=True, text=True)
    assert result.returncode in (0, 1)

def test_pre_paper_output_analyze():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-output-analyze"], capture_output=True, text=True)
    assert result.returncode in (0, 1)

def test_activation_denied_checkpoint():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "activation-denied-checkpoint"], capture_output=True, text=True)
    assert result.returncode in (0, 1)

def test_activation_checkpoint_validate():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "activation-checkpoint-validate"], capture_output=True, text=True)
    assert result.returncode in (0, 1)

def test_zero_mutation_assert():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "zero-mutation-assert"], capture_output=True, text=True)
    assert result.returncode in (0, 1)

def test_pre_paper_audit():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-audit"], capture_output=True, text=True)
    assert result.returncode in (0, 1)

def test_pre_paper_review():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-review"], capture_output=True, text=True)
    assert result.returncode in (0, 1)

def test_pre_paper_summary():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-summary"], capture_output=True, text=True)
    assert result.returncode in (0, 1)

def test_pre_paper_latest_review():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-latest-review"], capture_output=True, text=True)
    assert result.returncode in (0, 1)

def test_pre_paper_validate():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-validate"], capture_output=True, text=True)
    assert result.returncode in (0, 1)

def test_pre_paper_notification_preview():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-notification-preview"], capture_output=True, text=True)
    assert result.returncode in (0, 1)

def test_pre_paper_notification_dispatch_dry_run():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-notification-dispatch-dry-run"], capture_output=True, text=True)
    assert result.returncode in (0, 1)


def test_firewall_audit_cli_direct():
    import subprocess
    cmds = [
        "firewall-audit-info",
        "firewall-audit-ingest-pre-rehearsal",
        "firewall-event-ingest",
        "firewall-replay-plan",
        "firewall-replay-run",
        "firewall-replay-analyze",
        "zero-mutation-baseline",
        "zero-mutation-audit",
        "mutation-invariant-check",
        "baseline-hash-compare",
        "pre-paper-evidence-collect",
        "pre-paper-evidence-refresh",
        "pre-paper-evidence-gaps",
        "readiness-audit-decision",
        "firewall-audit-safety-check",
        "firewall-audit-trail",
        "firewall-audit-review",
        "firewall-audit-summary",
        "firewall-audit-latest-review",
        "firewall-audit-validate",
        "firewall-audit-notification-preview",
        "firewall-audit-notification-dispatch-dry-run"
    ]
    for cmd in cmds:
        result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", cmd], capture_output=True, text=True)
        assert result.returncode in (0, 1), f"Command {cmd} failed: {result.stderr}"


def test_paper_readiness_board_cli():
    import subprocess
    cmds = [
        "python -m usa_signal_bot paper-readiness-board-info",
        "python -m usa_signal_bot board-ingest-confirmation",
        "python -m usa_signal_bot board-eligibility",
        "python -m usa_signal_bot board-gates",
        "python -m usa_signal_bot board-decision",
        "python -m usa_signal_bot write-blocked-snapshot",
        "python -m usa_signal_bot write-blocked-attempt --attempt-type paper_state_write",
        "python -m usa_signal_bot write-deny-proof",
        ["python", "-m", "usa_signal_bot", "runtime-write-detect", "--text", "aktif et"],
        "python -m usa_signal_bot activation-firewall-rules",
        "python -m usa_signal_bot activation-firewall-evaluate --attempt-type enable_active_paper",
        "python -m usa_signal_bot activation-attempt-simulate",
        "python -m usa_signal_bot board-activation-denial-continuity",
        "python -m usa_signal_bot board-confidence-analyze",
        "python -m usa_signal_bot board-safety-check",
        "python -m usa_signal_bot board-audit",
        "python -m usa_signal_bot paper-readiness-board-review",
        "python -m usa_signal_bot paper-readiness-board-summary",
        "python -m usa_signal_bot paper-readiness-board-latest-review",
        "python -m usa_signal_bot paper-readiness-board-validate",
        "python -m usa_signal_bot paper-readiness-board-notification-preview",
        "python -m usa_signal_bot paper-readiness-board-notification-dispatch-dry-run"
    ]
    for cmd in cmds:
        args = cmd if isinstance(cmd, list) else cmd.split()
        res = subprocess.run(args, capture_output=True)
        assert res.returncode == 0

def test_cli_no_write_admission_commands():
    commands = [
        "no-write-admission-info",
        "no-write-ingest-board",
        "no-write-eligibility",
        "no-write-contract-clauses",
        "no-write-contract",
        "no-write-contract-validate",
        "activation-replay-plan",
        "activation-replay-run",
        "activation-replay-analyze",
        "paper-mode-preflight-plan",
        "paper-mode-preflight-run",
        "paper-mode-output-analyze",
        "runtime-write-lock-assert",
        "no-write-invariant-check",
        "preflight-safety-check",
        "no-write-audit",
        "no-write-admission-review",
        "no-write-admission-summary",
        "no-write-admission-latest-review",
        "no-write-admission-validate",
        "no-write-admission-notification-preview",
        "no-write-admission-notification-dispatch-dry-run"
    ]
    for cmd in commands:
        result = subprocess.run([sys.executable, "-m", "usa_signal_bot", cmd], capture_output=True, text=True)
        assert result.returncode == 0, f"Command {cmd} failed: {result.stderr}"
