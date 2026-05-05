with open('usa_signal_bot/core/health.py', 'r') as f:
    content = f.read()

checks_to_add = """
    results.append(check_portfolio_construction_config_health(context))
    results.append(check_allocation_methods_health(context))
    results.append(check_risk_budgeting_health(context))
    results.append(check_concentration_guards_health(context))
    results.append(check_portfolio_engine_health(context))
    results.append(check_portfolio_store_health(context))
"""

if 'check_portfolio_construction_config_health' not in content[:content.find('def run_health_checks')]:
    # We already appended the functions above, just need to hook them in.
    pass

if 'check_portfolio_construction_config_health(context)' not in content:
    content = content.replace('return results', checks_to_add + '\n    return results')

with open('usa_signal_bot/core/health.py', 'w') as f:
    f.write(content)
