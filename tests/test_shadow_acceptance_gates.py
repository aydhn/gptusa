def test_gates():
    from usa_signal_bot.paper_shadow_governance.acceptance_gates import default_shadow_acceptance_gates
    g = default_shadow_acceptance_gates({}, {})
    assert len(g) > 0
