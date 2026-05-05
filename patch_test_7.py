with open('tests/test_portfolio_candidates.py', 'r') as f:
    content = f.read()

content = content.replace('rs = RankedSignal(sig, 80.0, 50.0, 0.8, [], {})', 'rs = RankedSignal(sig, 80.0, 50.0, 0.8, [], {}, [], [], "utc")')

with open('tests/test_portfolio_candidates.py', 'w') as f:
    f.write(content)
