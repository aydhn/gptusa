import re
with open('tests/test_portfolio_candidates.py', 'r') as f:
    content = f.read()

# Fix instantiation of SelectedCandidate
content = re.sub(
    r'sel = SelectedCandidate\("s1", "AAPL", "1d", "Strat1", SignalAction.LONG, rank_score=80\)',
    'sel = SelectedCandidate("s1", "AAPL", "1d", "Strat1", SignalAction.LONG, 80.0, 0.8, 10.0, ["f1"])',
    content
)

# Fix instantiation of RiskDecision
content = re.sub(
    r'decision = RiskDecision\("d1", "AAPL", "1d", SignalAction.LONG, RiskDecisionStatus.APPROVED, 10, 1500, \["reason"\], \["flag"\], None\)',
    'from usa_signal_bot.core.enums import PositionSizingMethod, RiskSeverity\ndecision = RiskDecision("d1", "s1", "AAPL", "1d", "Strat1", SignalAction.LONG, RiskDecisionStatus.APPROVED, 10.0, 1500.0, PositionSizingMethod.FIXED_NOTIONAL, [], [], ["reason"], ["flag"], 50.0, RiskSeverity.LOW, "", "utc")',
    content
)

with open('tests/test_portfolio_candidates.py', 'w') as f:
    f.write(content)

with open('tests/test_allocation_methods.py', 'r') as f:
    content = f.read()

content = content.replace('res = allocate_equal_weight(req)', 'config = default_allocation_config()\n    config.max_candidate_weight = 1.0\n    res = allocate_equal_weight(req, config)')
content = content.replace('res = allocate_rank_weighted(req)', 'config = default_allocation_config()\n    config.max_candidate_weight = 1.0\n    res = allocate_rank_weighted(req, config)')

with open('tests/test_allocation_methods.py', 'w') as f:
    f.write(content)
