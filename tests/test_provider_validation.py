
from usa_signal_bot.data_providers.provider_validation import validate_provider_abstraction_context_report, validate_no_sensitive_data_in_provider_payload
from usa_signal_bot.data_providers.provider_abstraction import build_default_provider_abstraction_context

def test_provider_validation():
    ctx = build_default_provider_abstraction_context()
    rep = validate_provider_abstraction_context_report(ctx)
    assert rep.valid is True

    bad_payload = {"api_key": "123"}
    rep2 = validate_no_sensitive_data_in_provider_payload(bad_payload)
    assert rep2.valid is False
