def test_ingestion():
    from usa_signal_bot.backtesting.walk_forward.benchmark_comparison_ingestion import ingest_benchmark_comparison_review_payload
    res = ingest_benchmark_comparison_review_payload({})
    assert not res.ready_for_phase150
