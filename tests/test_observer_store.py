import pytest
from pathlib import Path
from usa_signal_bot.paper_observer.observer_store import (
    paper_observer_store_dir, write_paper_observer_review_json, read_paper_observer_review_json,
    paper_observer_store_summary
)
from usa_signal_bot.paper_observer.observer_report import build_paper_observer_review
from usa_signal_bot.paper_observer.observer_enrollment import build_observer_enrollment

def test_observer_store(tmp_path):
    enrollment = build_observer_enrollment("cand_1", "ticket_1", "APPROVED_FOR_NEXT_NON_EXECUTING_STAGE")
    review = build_paper_observer_review(enrollment)

    path = tmp_path / "reviews" / "test.json"
    path.parent.mkdir(parents=True)
    write_paper_observer_review_json(path, review)

    loaded = read_paper_observer_review_json(path)
    assert loaded["review_id"] == review.review_id

    summary = paper_observer_store_summary(tmp_path)
    assert "reviews" in summary
