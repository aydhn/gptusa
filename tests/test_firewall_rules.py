import pytest
from usa_signal_bot.paper_pre_rehearsal.firewall_rules import default_mutation_firewall_rules, validate_firewall_rules_complete

def test_default_rules():
    rules = default_mutation_firewall_rules()
    violations = validate_firewall_rules_complete(rules)
    assert len(violations) == 0
