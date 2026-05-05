with open('tests/test_portfolio_candidates.py', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.startswith('decision = RiskDecision'):
        lines[i] = '    ' + line

with open('tests/test_portfolio_candidates.py', 'w') as f:
    f.writelines(lines)
