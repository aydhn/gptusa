import pytest
from pathlib import Path
from usa_signal_bot.release.advanced_acceptance_report import build_advanced_acceptance_context, build_advanced_acceptance_full_review
from usa_signal_bot.release.advanced_acceptance_store import (
    advanced_acceptance_store_dir,
    write_advanced_acceptance_context_json,
    write_advanced_acceptance_full_review_json,
    read_advanced_acceptance_full_review_json
)

def test_advanced_acceptance_store(tmp_path):
    root = tmp_path / "data"
    context = build_advanced_acceptance_context()
    review = build_advanced_acceptance_full_review(context)

    ctx_path = root / "ctx.json"
    write_advanced_acceptance_context_json(ctx_path, context)
    assert ctx_path.exists()

    rev_path = root / "rev.json"
    write_advanced_acceptance_full_review_json(rev_path, review)
    assert rev_path.exists()

    loaded = read_advanced_acceptance_full_review_json(rev_path)
    assert loaded["review_id"] == review.review_id
