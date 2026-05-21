def test_evidence_index():
    from usa_signal_bot.paper_promotion_dossier.evidence_index import build_promotion_evidence_index
    idx = build_promotion_evidence_index({"candidate_id": "CAND-1"})
    assert idx.candidate_id == "CAND-1"
