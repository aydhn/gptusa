from usa_signal_bot.paper_shadow.shadow_signal_rehearsal import (
    generate_shadow_signals, generate_mock_shadow_signals,
    validate_shadow_signals_safe, shadow_signal_summary, shadow_signals_to_text
)
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context

def test_generate_shadow_signals():
    ctx = build_mock_shadow_simulation_context()
    signals = generate_shadow_signals(ctx)
    assert len(signals) == 3

def test_generate_mock_shadow_signals():
    signals = generate_mock_shadow_signals(["MSFT", "TSLA"])
    assert len(signals) == 2
    assert signals[0].symbol == "MSFT"

def test_validate_shadow_signals_safe():
    signals = generate_mock_shadow_signals()
    assert len(validate_shadow_signals_safe(signals)) == 0
    signals[0].reason = "Bu kesin alım."
    assert len(validate_shadow_signals_safe(signals)) == 1

def test_shadow_signal_summary():
    signals = generate_mock_shadow_signals()
    s = shadow_signal_summary(signals)
    assert s["count"] == 3

def test_shadow_signals_to_text():
    signals = generate_mock_shadow_signals()
    assert "count=3" in shadow_signals_to_text(signals)
