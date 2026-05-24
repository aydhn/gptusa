import pytest
from usa_signal_bot.runtime_lifecycle.startup_check_runner import StartupCheckRunner

def test_startup_check_runner():
    runner = StartupCheckRunner()
    report = runner.run_all_checks()

    assert report.total_checks > 10
    assert report.failed_checks == 0
    assert report.blocked_checks == 0
    assert report.execution_performed is False
    assert report.network_used is False
    assert report.startup_checks_metadata_only is True

    errors = runner.validate_startup_report_safety(report)
    assert len(errors) == 0

def test_startup_check_safety_validation():
    runner = StartupCheckRunner()
    report = runner.run_all_checks()
    report.execution_performed = True

    errors = runner.validate_startup_report_safety(report)
    assert len(errors) > 0
