def validate_regime_feature_engineering_context_safety(ctx) -> list[str]:
    if ctx.produces_trade_signal: return ["unsafe"]
    return []

def regime_feature_text_has_trade_or_execution_language(t):
    return "buy" in t.lower()
