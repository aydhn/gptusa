import pytest
from pathlib import Path
from usa_signal_bot.paper_readiness_confirmation.confirmation_store import (
    write_confirmation_queue_item_json,
    write_human_review_bundle_json,
    confirmation_queue_dir,
    human_review_bundles_dir
)
from usa_signal_bot.paper_readiness_confirmation.confirmation_queue import build_default_confirmation_queue_item
from usa_signal_bot.paper_readiness_confirmation.human_review_bundle import build_human_review_bundle

def test_write_confirmation_queue_item_json(tmp_path):
    q_dir = confirmation_queue_dir(tmp_path)
    q = build_default_confirmation_queue_item()
    p = write_confirmation_queue_item_json(q_dir, q)
    assert p.exists()

def test_write_human_review_bundle_json(tmp_path):
    b_dir = human_review_bundles_dir(tmp_path)
    q = build_default_confirmation_queue_item()
    b = build_human_review_bundle(q)
    p = write_human_review_bundle_json(b_dir, b)
    assert p.exists()
