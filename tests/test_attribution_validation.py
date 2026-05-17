import pytest
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent
from usa_signal_bot.attribution.attribution_validation import (
    validate_attribution_events_report, validate_no_live_execution_language_in_attribution,
    validate_no_broker_execution_fields_in_attribution, validate_no_sensitive_data_in_attribution_payload
)

def test_validate_attribution_events_report():
    events = [
        AttributionTradeEvent(event_id="e1", symbol="", net_pnl_usd=100.0), # invalid
        AttributionTradeEvent(event_id="e2", symbol="AAPL", total_cost_usd=-10.0), # invalid
    ]
    report = validate_attribution_events_report(events)
    assert not report.valid
    assert report.error_count == 2

def test_validate_no_live_execution_language():
    text_ok = "This is a dry run simulation for MSFT."
    text_bad = "Sent to broker for MSFT."

    report1 = validate_no_live_execution_language_in_attribution(text_ok)
    assert report1.valid

    report2 = validate_no_live_execution_language_in_attribution(text_bad)
    assert not report2.valid
    assert report2.blocked_count == 1

def test_validate_no_broker_execution_fields():
    payload_ok = {"symbol": "AAPL", "net_pnl": 100}
    payload_bad = {"symbol": "AAPL", "broker_order_id": "12345"}

    report1 = validate_no_broker_execution_fields_in_attribution(payload_ok)
    assert report1.valid

    report2 = validate_no_broker_execution_fields_in_attribution(payload_bad)
    assert not report2.valid

def test_validate_no_sensitive_data():
    payload_ok = {"symbol": "AAPL"}
    payload_bad = {"symbol": "AAPL", "api_key": "12345"}

    report1 = validate_no_sensitive_data_in_attribution_payload(payload_ok)
    assert report1.valid

    report2 = validate_no_sensitive_data_in_attribution_payload(payload_bad)
    assert not report2.valid
