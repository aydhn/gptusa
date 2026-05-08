import tempfile
from pathlib import Path
from usa_signal_bot.observability.local_logger import LocalObservabilityLogger, read_observability_events_jsonl, sanitize_log_payload

def test_local_logger():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td)
        logger = LocalObservabilityLogger(p)
        logger.info("src", "msg", {"foo": "bar", "api_key": "123"})

        events = read_observability_events_jsonl(logger.jsonl_log_path())
        assert len(events) == 1
        assert events[0]["message"] == "msg"
        assert events[0]["payload"]["foo"] == "bar"
        assert events[0]["payload"]["api_key"] == "[REDACTED]"

        assert logger.text_log_path().exists()
