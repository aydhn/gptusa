with open('usa_signal_bot/core/config_schema.py', 'r') as f:
    content = f.read()

validation_code = """
def validate_portfolio_construction_config(config: 'PortfolioConstructionConfig') -> None:
    if not config.enabled:
        return
    if not config.available_methods:
        raise ValueError("available_methods cannot be empty.")
    if not (0 <= config.max_total_allocation_pct <= 1):
        raise ValueError("max_total_allocation_pct must be between 0 and 1.")
    if not (0 <= config.cash_buffer_pct <= 1):
        raise ValueError("cash_buffer_pct must be between 0 and 1.")
    if not config.warn_not_optimizer:
        raise ValueError("warn_not_optimizer must be true.")
    if not config.warn_not_investment_advice:
        raise ValueError("warn_not_investment_advice must be true.")

def validate_allocation_limits_config(config: 'AllocationLimitsConfig') -> None:
    if not config.enabled:
        return
    if config.max_total_candidates <= 0:
        raise ValueError("max_total_candidates must be positive.")
    if config.min_candidate_weight > config.max_candidate_weight:
        raise ValueError("min_candidate_weight cannot be greater than max_candidate_weight.")

def validate_concentration_guards_config(config: 'ConcentrationGuardsConfig') -> None:
    if not config.enabled:
        return
    if not config.cap_breaches and not config.reject_breaches:
        print("Warning: Concentration guards enabled but neither cap nor reject breaches is active.")

def validate_app_config(config: AppConfig) -> None:
"""

if 'def validate_portfolio_construction_config' not in content:
    content = content.replace('def validate_app_config(config: AppConfig) -> None:', validation_code)

    # Add to validate_app_config
    if 'validate_portfolio_construction_config(config.portfolio_construction)' not in content:
        hook = """
    if config.portfolio_construction:
        validate_portfolio_construction_config(config.portfolio_construction)
    if config.allocation_limits:
        validate_allocation_limits_config(config.allocation_limits)
    if config.concentration_guards:
        validate_concentration_guards_config(config.concentration_guards)
"""
        content = content.replace('def validate_app_config(config: AppConfig) -> None:', 'def validate_app_config(config: AppConfig) -> None:\n' + hook)

with open('usa_signal_bot/core/config_schema.py', 'w') as f:
    f.write(content)
