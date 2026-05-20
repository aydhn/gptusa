import pytest
from usa_signal_bot.paper_dry_run_bridge.dry_run_context import build_mock_dry_run_bridge_context
from usa_signal_bot.paper_dry_run_bridge.bridge_session_runner import SupervisedDryRunBridgeRunner
from usa_signal_bot.paper_dry_run_bridge.dry_run_validation import (
    validate_dry_run_context_report,
    validate_dry_run_session_report,
    validate_no_sensitive_data_in_dry_run_payload,
    validate_no_live_execution_language_in_dry_run,
    validate_no_paper_state_mutation_fields_in_dry_run,
    validate_no_broker_execution_fields_in_dry_run,
    dry_run_bridge_validation_report_to_text,
    assert_dry_run_bridge_valid
)

def test_dry_run_validation():
    ctx = build_mock_dry_run_bridge_context()

    rep1 = validate_dry_run_context_report(ctx)
    assert rep1.valid is True

    ctx_bad = build_mock_dry_run_bridge_context()
    ctx_bad.allow_paper_orders = True
    rep_bad = validate_dry_run_context_report(ctx_bad)
    assert rep_bad.valid is False

    payload_sensitive = {"api_key": "mysecret"}
    rep_sens = validate_no_sensitive_data_in_dry_run_payload(payload_sensitive)
    assert rep_sens.valid is False

    text_bad = "This is definitely a live approved order."
    rep_text = validate_no_live_execution_language_in_dry_run(text_bad)
    assert rep_text.valid is False

    payload_mut = {"paper_state_committed": True}
    rep_mut = validate_no_paper_state_mutation_fields_in_dry_run(payload_mut)
    assert rep_mut.valid is False

    payload_brok = {"broker_order_id": "123"}
    rep_brok = validate_no_broker_execution_fields_in_dry_run(payload_brok)
    assert rep_brok.valid is False

    assert "VALID" in dry_run_bridge_validation_report_to_text(rep1)

    with pytest.raises(ValueError):
        assert_dry_run_bridge_valid(rep_bad)
