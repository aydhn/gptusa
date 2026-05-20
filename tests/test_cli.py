import subprocess
import sys
import pytest

def run_cli_command(command: list[str]) -> int:
    result = subprocess.run([sys.executable, "-m", "usa_signal_bot"] + command, capture_output=True)
    return result.returncode

def test_dry_run_bridge_info_cli():
    assert run_cli_command(["dry-run-bridge-info"]) == 0

def test_dry_run_ingest_quarantine_cli():
    assert run_cli_command(["dry-run-ingest-quarantine"]) == 0

def test_dry_run_ingest_ticket_cli():
    assert run_cli_command(["dry-run-ingest-ticket"]) == 0

def test_dry_run_ingest_bridge_plan_cli():
    assert run_cli_command(["dry-run-ingest-bridge-plan"]) == 0

def test_dry_run_paper_snapshot_cli():
    assert run_cli_command(["dry-run-paper-snapshot"]) == 0

def test_dry_run_context_cli():
    assert run_cli_command(["dry-run-context"]) == 0

def test_dry_run_proposals_cli():
    assert run_cli_command(["dry-run-proposals"]) == 0

def test_dry_run_risk_evaluate_cli():
    assert run_cli_command(["dry-run-risk-evaluate"]) == 0

def test_dry_run_notification_preview_cli():
    assert run_cli_command(["dry-run-notification-preview"]) == 0

def test_dry_run_operation_monitor_cli():
    assert run_cli_command(["dry-run-operation-monitor", "--operation", "send_paper_order"]) == 0

def test_dry_run_blocked_telemetry_cli():
    assert run_cli_command(["dry-run-blocked-telemetry"]) == 0

def test_human_review_checkpoint_cli():
    assert run_cli_command(["human-review-checkpoint"]) == 0

def test_human_checkpoint_validate_cli():
    assert run_cli_command(["human-checkpoint-validate"]) == 0

def test_dry_run_session_run_cli():
    assert run_cli_command(["dry-run-session-run", "--mode", "full_supervised_dry_run"]) == 0

def test_dry_run_session_analyze_cli():
    assert run_cli_command(["dry-run-session-analyze"]) == 0

def test_bridge_telemetry_report_cli():
    assert run_cli_command(["bridge-telemetry-report"]) == 0

def test_dry_run_session_registry_cli():
    assert run_cli_command(["dry-run-session-registry"]) == 0

def test_dry_run_bridge_review_cli():
    assert run_cli_command(["dry-run-bridge-review"]) == 0

def test_dry_run_bridge_summary_cli():
    assert run_cli_command(["dry-run-bridge-summary"]) == 0

def test_dry_run_bridge_latest_review_cli():
    assert run_cli_command(["dry-run-bridge-latest-review"]) == 0

def test_dry_run_bridge_validate_cli():
    assert run_cli_command(["dry-run-bridge-validate", "--latest-review"]) in [0, 1]

def test_dry_run_bridge_notification_preview_cli():
    assert run_cli_command(["dry-run-bridge-notification-preview", "--latest-review"]) in [0, 1]

def test_dry_run_bridge_notification_dispatch_dry_run_cli():
    assert run_cli_command(["dry-run-bridge-notification-dispatch-dry-run", "--latest-review"]) in [0, 1]
