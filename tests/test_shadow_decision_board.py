def test_decision():
    from usa_signal_bot.paper_shadow_governance.decision_board import ShadowRehearsalDecisionBoard
    from usa_signal_bot.core.enums import ShadowComparisonOutcome
    from usa_signal_bot.paper_shadow_governance.shadow_governance_models import ShadowAcceptanceScorecard, ShadowAcceptanceStatus, utc_now_iso
    sc = ShadowAcceptanceScorecard("sc", utc_now_iso(), "b", "c", ShadowAcceptanceStatus.PASS, 100, 0, 0, 0, 0, {}, [], True, False, False, False, False, [], [])
    d = ShadowRehearsalDecisionBoard().decide_from_scorecard(sc, ShadowComparisonOutcome.CANDIDATE_BETTER)
    assert d.decision.value == "ACCEPT_AS_SANDBOXED_PAPER_CANDIDATE"
