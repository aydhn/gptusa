def test_ingestion():
    from usa_signal_bot.paper_shadow_governance.session_ingestion import ingest_shadow_sessions
    res = ingest_shadow_sessions({"session_id": "b"}, {"session_id": "c"})
    assert res["baseline"]["session_id"] == "b"
