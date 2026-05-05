with open('tests/test_portfolio_candidates.py', 'r') as f:
    content = f.read()

content = content.replace('from usa_signal_bot.strategies.ranking_store import RankedSignal', 'from usa_signal_bot.strategies.signal_ranking import RankedSignal')

with open('tests/test_portfolio_candidates.py', 'w') as f:
    f.write(content)
