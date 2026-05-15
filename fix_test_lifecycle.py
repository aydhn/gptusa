def fix():
    with open('usa_signal_bot/regime_costs/lifecycle_regime_cost.py', 'r') as f:
        content = f.read()

    # The issue is "SPLIT" is in "post_split", so "SPLIT" condition matches before "POST_SPLIT".
    # Need to reverse their order.

    content = content.replace(
'''    if "SPLIT" in ca or "DIVIDEND" in ca or "PENDING" in ca:
        return CostLifecycleRegime.CORPORATE_ACTION_WATCH
    if "POST_SPLIT" in ca:
        return CostLifecycleRegime.POST_SPLIT_WINDOW''',
'''    if "POST_SPLIT" in ca:
        return CostLifecycleRegime.POST_SPLIT_WINDOW
    if "SPLIT" in ca or "DIVIDEND" in ca or "PENDING" in ca:
        return CostLifecycleRegime.CORPORATE_ACTION_WATCH'''
    )
    with open('usa_signal_bot/regime_costs/lifecycle_regime_cost.py', 'w') as f:
        f.write(content)

fix()
