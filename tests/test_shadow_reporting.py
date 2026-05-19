import pytest
from usa_signal_bot.paper_shadow.shadow_reporting import (
    shadow_context_to_text,
    paper_shadow_limitations_text
)
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context

def test_shadow_reporting():
    ctx = build_mock_shadow_simulation_context()
    text = shadow_context_to_text(ctx)
    assert "Shadow Simulation Context" in text

    limits = paper_shadow_limitations_text()
    assert "PAPER-SHADOW LIMITATIONS & DISCLAIMERS" in limits
