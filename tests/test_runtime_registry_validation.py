import pytest
from usa_signal_bot.advanced_runtime.runtime_registry_validation import validate_no_execution_language_in_runtime_registry_text

def test_val():
    assert validate_no_execution_language_in_runtime_registry_text("test").valid is True
    assert validate_no_execution_language_in_runtime_registry_text("emir gönderildi").valid is False
