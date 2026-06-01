from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_prototype_store import write_ensemble_prototype_full_review_json, read_ensemble_prototype_full_review_json
from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_prototype_report import build_ensemble_prototype_full_review
import tempfile
from pathlib import Path

def test_ensemble_prototype_store():
    review = build_ensemble_prototype_full_review()
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "review.json"
        write_ensemble_prototype_full_review_json(path, review)
        assert path.exists()
        loaded = read_ensemble_prototype_full_review_json(path)
        assert loaded["review_id"] == review.review_id
