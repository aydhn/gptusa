import subprocess

def run_cli_command(command):
    result = subprocess.run(["python", "-m", "usa_signal_bot", command], capture_output=True, text=True)
    return result

def test_paper_observer_info():
    res = run_cli_command("paper-observer-info")
    assert res.returncode == 0
    assert "Paper Observer Subsystem" in res.stdout

def test_observer_ingest_controlled_planning():
    res = run_cli_command("observer-ingest-controlled-planning")
    assert res.returncode == 0

def test_observer_eligibility():
    res = run_cli_command("observer-eligibility")
    assert res.returncode == 0

def test_observer_enrollment():
    res = run_cli_command("observer-enrollment")
    assert res.returncode == 0

def test_locked_observer_policy():
    res = run_cli_command("locked-observer-policy")
    assert res.returncode == 0

def test_observer_paper_snapshot():
    res = run_cli_command("observer-paper-snapshot")
    assert res.returncode == 0

def test_observer_runtime_context():
    res = run_cli_command("observer-runtime-context")
    assert res.returncode == 0

def test_observer_signal_mirror():
    res = run_cli_command("observer-signal-mirror")
    assert res.returncode == 0

def test_observer_proposals():
    res = run_cli_command("observer-proposals")
    assert res.returncode == 0

def test_observer_risk_mirror():
    res = run_cli_command("observer-risk-mirror")
    assert res.returncode == 0

def test_observer_notification_preview():
    res = run_cli_command("observer-notification-preview")
    assert res.returncode == 0

def test_observer_parallel_monitor():
    res = run_cli_command("observer-parallel-monitor")
    assert res.returncode == 0

def test_observer_drift_detect():
    res = run_cli_command("observer-drift-detect")
    assert res.returncode == 0

def test_observer_blocked_operation_guard():
    res = run_cli_command("observer-blocked-operation-guard")
    assert res.returncode == 0

def test_observer_runtime_safety_check():
    res = run_cli_command("observer-runtime-safety-check")
    assert res.returncode == 0

def test_observer_monitoring_analyze():
    res = run_cli_command("observer-monitoring-analyze")
    assert res.returncode == 0

def test_observer_session_registry():
    res = run_cli_command("observer-session-registry")
    assert res.returncode == 0

def test_observer_audit():
    res = run_cli_command("observer-audit")
    assert res.returncode == 0

def test_paper_observer_review():
    res = run_cli_command("paper-observer-review")
    assert res.returncode == 0

def test_paper_observer_summary():
    res = run_cli_command("paper-observer-summary")
    assert res.returncode == 0

def test_paper_observer_latest_review():
    res = run_cli_command("paper-observer-latest-review")
    assert res.returncode == 0

def test_paper_observer_validate():
    res = run_cli_command("paper-observer-validate")
    assert res.returncode == 0

def test_paper_observer_notification_preview_cmd():
    res = run_cli_command("paper-observer-notification-preview-cmd")
    assert res.returncode == 0

def test_paper_observer_notification_dispatch_dry_run():
    res = run_cli_command("paper-observer-notification-dispatch-dry-run")
    assert res.returncode == 0
