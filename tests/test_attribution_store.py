import pytest
from pathlib import Path
import json
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent
from usa_signal_bot.attribution.attribution_store import (
    write_attribution_events_jsonl, attribution_store_summary
)

def test_write_attribution_events_jsonl(tmp_path):
    events = [AttributionTradeEvent(event_id="e1", symbol="AAPL", net_pnl_usd=100.0)]
    f = write_attribution_events_jsonl(tmp_path / "events.jsonl", events)
    assert f.exists()

    with open(f, "r") as file:
        data = json.loads(file.readline())
        assert data["symbol"] == "AAPL"

def test_attribution_store_summary(tmp_path):
    from usa_signal_bot.attribution.attribution_store import attribution_reviews_dir
    reviews_dir = attribution_reviews_dir(tmp_path)
    (reviews_dir / "r1.json").touch()
    (reviews_dir / "r2.json").touch()

    summary = attribution_store_summary(tmp_path)
    assert summary["reviews_count"] == 2
