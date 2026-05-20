import pytest
from usa_signal_bot.paper_shadow_governance.session_comparator import compare_shadow_sessions
from usa_signal_bot.core.enums import ShadowComparisonOutcome

def test_compare_shadow_sessions():
    bp = {"metrics": {"simulated_pnl_usd": 100.0, "blocked_intent_count": 5}}
    cp = {"metrics": {"simulated_pnl_usd": 150.0, "blocked_intent_count": 2}}
    report = compare_shadow_sessions(bp, cp)
    assert report.outcome == ShadowComparisonOutcome.CANDIDATE_BETTER
