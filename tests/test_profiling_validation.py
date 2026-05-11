import pytest
from usa_signal_bot.core.enums import ResourceProfileScope, ResourceProfileStatus
from usa_signal_bot.profiling.profiling_models import ResourceProfile
from usa_signal_bot.profiling.profiling_validation import validate_resource_profile_report, validate_no_live_execution_language_in_profiling

def test_validate_resource_profile_report():
    prof = ResourceProfile("id", ResourceProfileScope.TASK, "t", ResourceProfileStatus.COMPLETED, None, None, -1.0, 0, 0, 0, 0, 0, 0, 0, [], [], [])
    report = validate_resource_profile_report(prof)

    assert not report.valid
    assert any(i.field == "wall_time_seconds" for i in report.issues)

def test_validate_no_live_execution_language():
    report = validate_no_live_execution_language_in_profiling("This is investment advice")
    assert not report.valid
    assert report.blocked_count == 1

    report2 = validate_no_live_execution_language_in_profiling("Local review only")
    assert report2.valid

def test_validate_external_telemetry():
    prof = ResourceProfile("id", ResourceProfileScope.TASK, "t", ResourceProfileStatus.COMPLETED, None, None, 1.0, 0, 0, 0, 0, 0, 0, 0, [], [], [], {"sentry_dsn": "https://..."})
    report = validate_resource_profile_report(prof)
    assert not report.valid
    assert any("telemetry" in i.message.lower() for i in report.issues)
