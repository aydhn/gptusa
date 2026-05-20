def test_evidence():
    from usa_signal_bot.paper_shadow_governance.evidence_pack import build_shadow_evidence_pack
    p = build_shadow_evidence_pack({}, {})
    assert not p.evidence_complete
