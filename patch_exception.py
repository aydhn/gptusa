with open("usa_signal_bot/core/exceptions.py", "r") as f:
    content = f.read()

# Make PortfolioRiskValidationError extend Exception to avoid USASignalBotError missing issue
if "class PortfolioRiskValidationError(Exception):" not in content:
    content = content.replace("class PortfolioRiskValidationError(PortfolioRiskReportingError): pass", "class PortfolioRiskValidationError(Exception): pass")

with open("usa_signal_bot/core/exceptions.py", "w") as f:
    f.write(content)
