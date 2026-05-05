import re
with open('usa_signal_bot/portfolio/portfolio_candidates.py', 'r') as f:
    content = f.read()

content = content.replace('rank_score=rs.final_score,', 'rank_score=rs.rank_score,')

with open('usa_signal_bot/portfolio/portfolio_candidates.py', 'w') as f:
    f.write(content)
