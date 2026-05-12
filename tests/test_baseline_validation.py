import pytest
from usa_signal_bot.core.exceptions import PerformanceBaselineValidationError
from usa_signal_bot.performance.baseline_validation import (
    validate_no_sensitive_data_in_performance_payload,
    validate_no_live_execution_language_in_performance,
    validate_no_external_telemetry_fields_in_performance,
    assert_performance_valid
)

def test_validate_no_sensitive_data_in_performance_payload():
    bad = {"my_secret_token": "actual_secret_value"}
    rep = validate_no_sensitive_data_in_performance_payload(bad)
    assert not rep.valid

    good = {"my_secret_token": "***REDACTED***"}
    rep2 = validate_no_sensitive_data_in_performance_payload(good)
    assert rep2.valid

def test_validate_no_live_execution_language_in_performance():
    bad = "This has been live approved and sent to broker."
    rep = validate_no_live_execution_language_in_performance(bad)
    assert not rep.valid
    assert rep.error_count >= 2

    good = "This is a local operational performance review."
    rep2 = validate_no_live_execution_language_in_performance(good)
    assert rep2.valid

def test_validate_no_external_telemetry_fields_in_performance():
    bad = {"prometheus_url": "http://some.site"}
    rep = validate_no_external_telemetry_fields_in_performance(bad)
    assert not rep.valid

    good = {"metrics": {"wall_time": 10}}
    rep2 = validate_no_external_telemetry_fields_in_performance(good)
    assert rep2.valid

def test_assert_performance_valid():
    bad = {"prometheus_url": "http://some.site"}
    rep = validate_no_external_telemetry_fields_in_performance(bad)
    with pytest.raises(PerformanceBaselineValidationError):
        assert_performance_valid(rep)
