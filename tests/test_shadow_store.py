import tempfile
from pathlib import Path
from usa_signal_bot.paper_shadow.shadow_store import (
    write_shadow_context_json, write_shadow_rehearsal_review_json,
    read_shadow_rehearsal_review_json, list_shadow_rehearsal_reviews,
    shadow_reviews_dir
)
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalReview, ShadowReportType

def test_shadow_store():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_root = Path(tmpdir)

        ctx = build_mock_shadow_simulation_context()
        review = ShadowRehearsalReview(
            review_id="r1", created_at_utc="2023-01-01",
            report_type=ShadowReportType.FULL_SHADOW_REHEARSAL_REVIEW,
            sessions=[], output_paths={}, warnings=[], errors=[]
        )

        # Test write
        rev_path = shadow_reviews_dir(data_root) / f"{review.review_id}.json"
        write_shadow_rehearsal_review_json(rev_path, review)

        # Test read
        data = read_shadow_rehearsal_review_json(rev_path)
        assert data["review_id"] == "r1"

        # Test list
        reviews = list_shadow_rehearsal_reviews(data_root)
        assert len(reviews) == 1
