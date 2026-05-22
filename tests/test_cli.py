
import subprocess
import sys

def run_command(args):
    return subprocess.run([sys.executable, "-m", "usa_signal_bot"] + args, capture_output=True, text=True)

def test_dry_admission_info():
    result = run_command(["dry-admission-info"])
    assert result.returncode == 0
    assert "Paper-Mode Dry Admission Rehearsal Module" in result.stdout

def test_dry_admission_ingest_no_write():
    result = run_command(["dry-admission-ingest-no-write"])
    assert result.returncode == 0

def test_dry_admission_eligibility():
    result = run_command(["dry-admission-eligibility"])
    assert result.returncode == 0

def test_dry_admission_plan():
    result = run_command(["dry-admission-plan"])
    assert result.returncode == 0

def test_dry_admission_run():
    result = run_command(["dry-admission-run"])
    assert result.returncode == 0

def test_dry_admission_output_analyze():
    result = run_command(["dry-admission-output-analyze"])
    assert result.returncode == 0

def test_write_lock_refresh():
    result = run_command(["write-lock-refresh"])
    assert result.returncode == 0

def test_write_lock_refresh_validate():
    result = run_command(["write-lock-refresh-validate"])
    assert result.returncode == 0

def test_human_ledger_entry():
    result = run_command(["human-ledger-entry", "NOT_ACTIVATION_APPROVAL", "--note", "acknowledged no activation"])
    assert result.returncode == 0

def test_human_approval_ledger():
    result = run_command(["human-approval-ledger"])
    assert result.returncode == 0

def test_human_approval_validate():
    result = run_command(["human-approval-validate"])
    assert result.returncode == 0

def test_approval_reconcile():
    result = run_command(["approval-reconcile"])
    assert result.returncode == 0

def test_no_write_continuity():
    result = run_command(["no-write-continuity"])
    assert result.returncode == 0

def test_dry_admission_safety_check():
    result = run_command(["dry-admission-safety-check"])
    assert result.returncode == 0

def test_dry_admission_audit():
    result = run_command(["dry-admission-audit"])
    assert result.returncode == 0

def test_dry_admission_review():
    result = run_command(["dry-admission-review"])
    assert result.returncode == 0

def test_dry_admission_summary():
    result = run_command(["dry-admission-summary"])
    assert result.returncode == 0

def test_dry_admission_latest_review():
    result = run_command(["dry-admission-latest-review"])
    assert result.returncode in [0, 1]

def test_dry_admission_validate():
    result = run_command(["dry-admission-validate", "--latest-review"])
    assert result.returncode in [0, 1]

def test_dry_admission_notification_preview():
    result = run_command(["dry-admission-notification-preview"])
    assert result.returncode in [0, 1]

def test_dry_admission_notification_dispatch_dry_run():
    result = run_command(["dry-admission-notification-dispatch-dry-run"])
    assert result.returncode in [0, 1]
