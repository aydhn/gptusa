def test_gates():
    from usa_signal_bot.paper_promotion_dossier.safety_board_gates import default_final_safety_board_gates
    from usa_signal_bot.paper_promotion_dossier.dossier_builder import build_promotion_dossier_from_observer_governance
    d = build_promotion_dossier_from_observer_governance({"candidate_id": "CAND-1"})
    gates = default_final_safety_board_gates(d)
    assert len(gates) > 0
