import pytest
from usa_signal_bot.backtesting.benchmark_comparison.benchmark_comparison_validation import (
    validate_no_sensitive_data_in_benchmark_payload
)

def test_validation():
    rep = validate_no_sensitive_data_in_benchmark_payload({"test": "data"})
    assert rep.valid is True

    rep_bad = validate_no_sensitive_data_in_benchmark_payload({"api_key": "123"})
    assert rep_bad.valid is False
