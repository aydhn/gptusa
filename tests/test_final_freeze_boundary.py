import pytest
from usa_signal_bot.release.final_freeze_boundary import build_final_freeze_boundary_rules, build_final_freeze_boundary_result

def test_final_freeze_boundary():
    # default context
    rules = build_final_freeze_boundary_rules({})
    res = build_final_freeze_boundary_result(rules)
    assert res.boundary_passed == True
    assert res.advanced_acceptance_only == True
    assert res.no_live_trading == True
    assert res.no_paper_state_mutation == True
    assert res.no_deployment == True

    # invalid context
    bad_rules = build_final_freeze_boundary_rules({"live_trading_enabled": True})
    bad_res = build_final_freeze_boundary_result(bad_rules)
    assert bad_res.boundary_passed == False
    assert bad_res.no_live_trading == False
