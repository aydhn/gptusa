def test_extract():
    from usa_signal_bot.paper_shadow_governance.metric_extractor import extract_shadow_metrics
    m = extract_shadow_metrics({"metrics": {"signal_count": 5}})
    assert m["signal_count"] == 5
