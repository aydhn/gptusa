from usa_signal_bot.release_packaging.governance_ingestion import governance_candidate_packaging_allowed

def test_governance_ingestion():
    allowed, reasons = governance_candidate_packaging_allowed({"allowed_for_auto_apply": True})
    assert allowed is False
    assert len(reasons) > 0
