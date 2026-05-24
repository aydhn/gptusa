from usa_signal_bot.paper_readiness_board_dossier.shadow_launch_blocker_rules import default_shadow_launch_blocker_rules

def test_default_shadow_launch_blocker_rules():
    rules = default_shadow_launch_blocker_rules()
    assert len(rules) == 11
    assert all(r.enabled for r in rules)
    assert all(r.blocking for r in rules)
