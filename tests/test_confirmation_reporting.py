from usa_signal_bot.paper_readiness_confirmation.confirmation_reporting import (
    readiness_confirmation_queue_item_to_text,
    readiness_confirmation_limitations_text
)
from usa_signal_bot.paper_readiness_confirmation.confirmation_queue import build_default_confirmation_queue_item

def test_readiness_confirmation_queue_item_to_text():
    q = build_default_confirmation_queue_item()
    t = readiness_confirmation_queue_item_to_text(q)
    assert q.queue_item_id in t

def test_readiness_confirmation_limitations_text():
    t = readiness_confirmation_limitations_text()
    assert "No broker" in t
    assert "No active paper" in t
