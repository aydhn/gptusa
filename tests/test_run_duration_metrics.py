from usa_signal_bot.observability.run_duration_metrics import summarize_duration_values

def test_duration_summary():
    s = summarize_duration_values([10.0, 20.0], "test")
    assert s.average_duration_seconds == 15.0
    assert s.run_count == 2
