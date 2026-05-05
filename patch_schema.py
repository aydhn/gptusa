import re

with open('usa_signal_bot/core/config_schema.py', 'r') as f:
    content = f.read()

# Make sure AppConfig has the new fields
if 'portfolio_construction: PortfolioConstructionConfig' not in content:
    app_config_pattern = r'class AppConfig:\n'
    new_app_config_fields = """class AppConfig:
    portfolio_construction: 'PortfolioConstructionConfig' = None
    allocation_limits: 'AllocationLimitsConfig' = None
    risk_budgeting: 'RiskBudgetingConfig' = None
    concentration_guards: 'ConcentrationGuardsConfig' = None
"""
    content = content.replace('class AppConfig:\n', new_app_config_fields)

with open('usa_signal_bot/core/config_schema.py', 'w') as f:
    f.write(content)
