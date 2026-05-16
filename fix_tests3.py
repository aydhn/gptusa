with open("tests/test_risk_budgeting.py", "r") as f:
    c = f.read()
c = c.replace('assert "BREACHED" in text', 'assert "EXHAUSTED" in text')
with open("tests/test_risk_budgeting.py", "w") as f:
    f.write(c)
