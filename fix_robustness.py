def fix():
    with open('usa_signal_bot/regime_costs/robustness_adapter.py', 'r') as f:
        content = f.read()

    # CombinedCostRegime doesn't have EXTREME, only HIGH_RISK, BLOCKED, etc.
    content = content.replace(
        "if snapshot.combined_regime in (CombinedCostRegime.HIGH_RISK, CombinedCostRegime.EXTREME):",
        "if snapshot.combined_regime in (CombinedCostRegime.HIGH_RISK, CombinedCostRegime.BLOCKED):"
    )

    with open('usa_signal_bot/regime_costs/robustness_adapter.py', 'w') as f:
        f.write(content)

fix()
