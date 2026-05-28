import pytest
import os
import shutil
from pathlib import Path
from usa_signal_bot.feature_engine.final_closure.final_closure_report import build_final_closure_full_review
from usa_signal_bot.feature_engine.final_closure.final_closure_store import (
    final_closure_store_dir, write_final_closure_full_review_json,
    read_final_closure_full_review_json, list_final_closure_reviews,
    get_latest_final_closure_review, final_closure_store_summary
)

def test_final_closure_store(tmp_path):
    d = tmp_path / "data"
    d.mkdir()

    review = build_final_closure_full_review()

    f = final_closure_store_dir(d) / "reviews"
    f.mkdir(parents=True, exist_ok=True)

    file_path = f / f"{review.review_id}.json"
    write_final_closure_full_review_json(file_path, review)

    loaded = read_final_closure_full_review_json(file_path)
    assert loaded["review_id"] == review.review_id

    reviews = list_final_closure_reviews(d)
    assert len(reviews) == 1

    latest = get_latest_final_closure_review(d)
    assert latest == file_path

    summary = final_closure_store_summary(d)
    assert summary["reviews"] == 1
