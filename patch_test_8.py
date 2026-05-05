with open('usa_signal_bot/portfolio/portfolio_candidates.py', 'r') as f:
    content = f.read()

content = content.replace('risk_score=rs.risk_penalty,', 'risk_score=rs.penalties.get("RISK_PENALTY", 50.0),')

with open('usa_signal_bot/portfolio/portfolio_candidates.py', 'w') as f:
    f.write(content)

with open('tests/test_portfolio_candidates.py', 'r') as f:
    content = f.read()

# Update RankedSignal instantiation
new_rs = 'rs = RankedSignal(sig, 80.0, 1, CandidateSelectionStatus.SELECTED, {}, {"RISK_PENALTY": 50.0}, {}, [], "utc")'
import re
content = re.sub(r'rs = RankedSignal\(.*?\)', new_rs, content)

with open('tests/test_portfolio_candidates.py', 'w') as f:
    f.write(content)
