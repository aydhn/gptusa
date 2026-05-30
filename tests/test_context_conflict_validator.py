import pytest
from usa_signal_bot.regime_classification.validation.context_conflict_validator import detect_conflicted_contexts

def test_detect_conflicted_contexts():
    comp_res = [
        {"classification": "conflicted_signal"},
        {"classification": "high_compatibility"}
    ]
    con = detect_conflicted_contexts(comp_res)
    assert len(con) == 1
