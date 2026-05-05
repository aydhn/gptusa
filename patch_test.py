import re
with open('tests/test_portfolio_candidates.py', 'r') as f:
    content = f.read()

# Remove the import of CandidateRiskProfile
content = content.replace(', CandidateRiskProfile', '')

# Replace usage
content = re.sub(
    r'profile = CandidateRiskProfile\("s1", "AAPL", "1d", "Strategy1", SignalAction.BUY, price=150.0, rank_score=90\)\s*\n\s*decision = RiskDecision\("d1", "AAPL", "1d", SignalAction.BUY, RiskDecisionStatus.APPROVED, 10, 1500, \["reason"\], \["flag"\], profile\)',
    'decision = RiskDecision("d1", "AAPL", "1d", SignalAction.BUY, RiskDecisionStatus.APPROVED, 10, 1500, ["reason"], ["flag"], None)\n    decision.price = 150.0\n    decision.rank_score = 90\n    decision.strategy_name = "Strategy1"',
    content,
    flags=re.MULTILINE
)

with open('tests/test_portfolio_candidates.py', 'w') as f:
    f.write(content)
