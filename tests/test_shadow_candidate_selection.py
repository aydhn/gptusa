import pytest
from usa_signal_bot.paper_shadow.shadow_candidate_selection import (
    select_shadow_candidates,
    rank_shadow_signals,
    shadow_candidates_to_text
)
from usa_signal_bot.paper_shadow.shadow_signal_rehearsal import generate_mock_shadow_signals

def test_shadow_candidate_selection():
    signals = generate_mock_shadow_signals(["AAPL", "MSFT", "GOOG"])
    signals[0].score = 40.0
    signals[1].score = 80.0
    signals[2].score = 90.0

    ranked = rank_shadow_signals(signals)
    assert ranked[0].symbol == "GOOG"

    cands = select_shadow_candidates(signals, min_score=50.0, max_candidates=2)
    assert len(cands) == 2
    assert cands[0].symbol == "GOOG"
    assert cands[1].symbol == "MSFT"

    text = shadow_candidates_to_text(cands)
    assert "Shadow Candidates" in text
