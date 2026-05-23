
from usa_signal_bot.paper_no_order_dossier.admission_blocker_rules import default_paper_admission_blocker_rules

def test_default_rules_are_blocking():
    rules = default_paper_admission_blocker_rules()
    assert len(rules) > 0
    for r in rules:
        assert r.blocking is True
        assert r.enabled is True
