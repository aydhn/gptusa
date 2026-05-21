from usa_signal_bot.paper_observation.observation_store import (
    write_observation_window_json, observation_store_summary, read_observation_review_json,
    write_observation_review_json, get_latest_observation_review,
    observation_windows_dir, observation_reviews_dir, observation_store_dir
)
from usa_signal_bot.paper_observation.observation_models import ObservationWindow, ObservationReview
import tempfile
from pathlib import Path

def test_observation_store():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        w = ObservationWindow("w1", "2023", "c1", "t1", "PLANNED", "FULL_SUPERVISED_OBSERVATION", None, None, 3, 3, [], [], 0, 0, False)
        w_path = observation_windows_dir(root) / "w1.json"
        write_observation_window_json(w_path, w)
        assert w_path.exists()

        rev = ObservationReview("r1", "2023", "FULL_OBSERVATION_REVIEW", [w], [], [], [], [], [], {})
        r_path = observation_reviews_dir(root) / "r1.json"
        write_observation_review_json(r_path, rev)
        assert r_path.exists()

        loaded = read_observation_review_json(r_path)
        assert loaded["review_id"] == "r1"

        latest = get_latest_observation_review(root)
        assert latest == r_path

        summ = observation_store_summary(root)
        assert summ["windows"] == 1
        assert summ["reviews"] == 1
