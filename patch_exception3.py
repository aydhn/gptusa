with open("usa_signal_bot/core/exceptions.py", "r") as f:
    content = f.read()

if "class PortfolioRiskValidationError(Exception): pass" not in content:
    content += "\nclass PortfolioRiskValidationError(Exception): pass\n"

with open("usa_signal_bot/core/exceptions.py", "w") as f:
    f.write(content)
