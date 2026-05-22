import subprocess
import pytest

def test_pre_paper_rehearsal_info():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-rehearsal-info"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "ACTIVE" in result.stdout

def test_pre_paper_ingest_final_handoff():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-ingest-final-handoff"], capture_output=True, text=True)
    assert result.returncode == 0

def test_pre_paper_eligibility():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-eligibility"], capture_output=True, text=True)
    assert result.returncode == 0

def test_pre_paper_plan():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-plan"], capture_output=True, text=True)
    assert result.returncode == 0

def test_pre_paper_baseline():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-baseline"], capture_output=True, text=True)
    assert result.returncode == 0

def test_mutation_firewall_rules():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "mutation-firewall-rules"], capture_output=True, text=True)
    assert result.returncode == 0

def test_mutation_firewall_evaluate():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "mutation-firewall-evaluate", "--attempt-type", "paper_state_write"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "BLOCKED" in result.stdout

def test_mutation_attempt_detect():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "mutation-attempt-detect", "--text", "paper'a uygula"], capture_output=True, text=True)
    assert result.returncode == 0

def test_forbidden_operation_simulate():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "forbidden-operation-simulate"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "BLOCKED" in result.stdout

def test_pre_paper_dry_run():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-dry-run"], capture_output=True, text=True)
    assert result.returncode == 0

def test_pre_paper_output_analyze():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-output-analyze"], capture_output=True, text=True)
    assert result.returncode == 0

def test_activation_denied_checkpoint():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "activation-denied-checkpoint"], capture_output=True, text=True)
    assert result.returncode == 0

def test_activation_checkpoint_validate():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "activation-checkpoint-validate"], capture_output=True, text=True)
    assert result.returncode == 0

def test_zero_mutation_assert():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "zero-mutation-assert"], capture_output=True, text=True)
    assert result.returncode == 0

def test_pre_paper_audit():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-audit"], capture_output=True, text=True)
    assert result.returncode == 0

def test_pre_paper_review():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-review"], capture_output=True, text=True)
    assert result.returncode == 0

def test_pre_paper_summary():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-summary"], capture_output=True, text=True)
    assert result.returncode == 0

def test_pre_paper_latest_review():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-latest-review"], capture_output=True, text=True)
    assert result.returncode == 0

def test_pre_paper_validate():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-validate"], capture_output=True, text=True)
    assert result.returncode == 0

def test_pre_paper_notification_preview():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-notification-preview"], capture_output=True, text=True)
    assert result.returncode == 0

def test_pre_paper_notification_dispatch_dry_run():
    result = subprocess.run(["python3", "-m", "usa_signal_bot.app.cli", "pre-paper-notification-dispatch-dry-run"], capture_output=True, text=True)
    assert result.returncode == 0
