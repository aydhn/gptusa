def test_report():
    from usa_signal_bot.paper_promotion_dossier.dossier_report import build_promotion_dossier_review
    from usa_signal_bot.paper_promotion_dossier.dossier_builder import build_promotion_dossier_from_observer_governance
    d = build_promotion_dossier_from_observer_governance({"candidate_id": "CAND-1"})
    r = build_promotion_dossier_review(d)
    assert len(r.dossiers) == 1
