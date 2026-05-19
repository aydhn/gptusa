import pytest
from usa_signal_bot.paper_shadow.shadow_signal_rehearsal import (
    generate_mock_shadow_signals,
    validate_shadow_signals_safe,
    shadow_signals_to_text
)

def test_shadow_signal_rehearsal():
    signals = generate_mock_shadow_signals(["AAPL", "MSFT"])
    assert len(signals) == 2
    assert signals[0].symbol == "AAPL"

    errors = validate_shadow_signals_safe(signals)
    assert not errors

    signals[0].reason = "Kesin al kardeşim"
    errors = validate_shadow_signals_safe(signals)
    assert len(errors) == 1

    text = shadow_signals_to_text(signals)
    assert "Shadow Signals" in text
