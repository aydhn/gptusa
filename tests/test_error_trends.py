from usa_signal_bot.observability.error_trends import build_error_trend_summary
import datetime

def test_error_trends():
    events = [{"severity": "ERROR", "message": "msg1", "source": "src1", "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}]
    s = build_error_trend_summary(events)
    assert s.error_count == 1
    assert s.status.value == "OK" # not over threshold
