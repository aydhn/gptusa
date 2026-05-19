def check_paper_shadow_health():
    from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context
    ctx = build_mock_shadow_simulation_context()
    if ctx.allow_real_orders or ctx.allow_broker_calls or ctx.allow_paper_state_mutation or ctx.allow_telegram_real_send:
        return "FAIL: Unsafe flags in shadow context"
    return "PASS"
