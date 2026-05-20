from usa_signal_bot.paper_shadow.shadow_candidate_selection import (
    select_shadow_candidates, rank_shadow_signals, filter_shadow_signals_by_safety,
    shadow_candidate_summary, shadow_candidates_to_text
)
from usa_signal_bot.paper_shadow.shadow_signal_rehearsal import generate_mock_shadow_signals

def test_select_shadow_candidates():
    signals = generate_mock_shadow_signals()
    signals[0].score = 40.0
    cands = select_shadow_candidates(signals, min_score=50.0)
    assert len(cands) == 2

def test_rank_shadow_signals():
    signals = generate_mock_shadow_signals()
    signals[0].score = 40.0
    signals[1].score = 90.0
    ranked = rank_shadow_signals(signals)
    assert ranked[0].score == 90.0

def test_filter_shadow_signals_by_safety():
    signals = generate_mock_shadow_signals()
    signals[0].reason = "Kesin kâr."
    safe = filter_shadow_signals_by_safety(signals)
    assert len(safe) == 2

def test_shadow_candidate_summary():
    signals = generate_mock_shadow_signals()
    s = shadow_candidate_summary(signals)
    assert s["count"] == 3

def test_shadow_candidates_to_text():
    signals = generate_mock_shadow_signals()
    assert "count=3" in shadow_candidates_to_text(signals)
