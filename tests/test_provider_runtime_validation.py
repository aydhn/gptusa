from usa_signal_bot.data_provider_runtime.provider_runtime_validation import validate_no_sensitive_data_in_provider_runtime_payload, validate_no_execution_language_in_provider_runtime_text

def test_validation():
    res = validate_no_sensitive_data_in_provider_runtime_payload({"data": "normal"})
    assert res.valid is True

    res2 = validate_no_sensitive_data_in_provider_runtime_payload({"api_key": "123"})
    assert res2.valid is False

    res3 = validate_no_execution_language_in_provider_runtime_text("this is a test")
    assert res3.valid is True

    res4 = validate_no_execution_language_in_provider_runtime_text("emir gönderildi")
    assert res4.valid is False
