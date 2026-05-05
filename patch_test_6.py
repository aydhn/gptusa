with open('tests/test_portfolio_candidates.py', 'r') as f:
    content = f.read()

content = content.replace('sig = StrategySignal("sig1", "Strat1", "AAPL", "1d", SignalAction.LONG, 150.0, 100.0, 0.8, [], "utc")', 'sig = StrategySignal("sig1", "Strat1", "AAPL", "1d", SignalAction.LONG, 150.0, 100.0, 0.8, [], "utc", {}, [])')

with open('tests/test_portfolio_candidates.py', 'w') as f:
    f.write(content)
