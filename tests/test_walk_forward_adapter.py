import unittest
from unittest.mock import patch, MagicMock
from usa_signal_bot.attribution.walk_forward_adapter import (
    build_attribution_by_walk_forward_window,
    attach_attribution_to_walk_forward_result,
    walk_forward_attribution_summary,
    walk_forward_attribution_warnings
)

class TestWalkForwardAdapter(unittest.TestCase):
    @patch("usa_signal_bot.attribution.walk_forward_adapter.build_attribution_review_from_backtest_result")
    def test_build_attribution_by_walk_forward_window(self, mock_build):
        mock_build.side_effect = ["review_0", "review_1"]
        result = {"windows": [{"id": 0}, {"id": 1}]}
        reviews = build_attribution_by_walk_forward_window(result)

        self.assertEqual(len(reviews), 2)
        self.assertEqual(reviews["window_0"], "review_0")
        self.assertEqual(reviews["window_1"], "review_1")
        mock_build.assert_any_call({"id": 0})
        mock_build.assert_any_call({"id": 1})
        self.assertEqual(mock_build.call_count, 2)

    @patch("usa_signal_bot.attribution.walk_forward_adapter.build_attribution_by_walk_forward_window")
    def test_attach_attribution_to_walk_forward_result_no_reviews(self, mock_build_by_window):
        mock_review = MagicMock()
        mock_review.review_id = "r_1"
        mock_review.scorecard = None
        mock_build_by_window.return_value = {"window_0": mock_review}

        result = {"existing": "data"}
        new_result = attach_attribution_to_walk_forward_result(result)

        self.assertIn("attribution_metadata", new_result)
        self.assertEqual(new_result["attribution_metadata"]["window_reviews"]["window_0"], "r_1")
        mock_build_by_window.assert_called_once_with(result)

    def test_attach_attribution_to_walk_forward_result_with_reviews(self):
        mock_review = MagicMock()
        mock_review.review_id = "r_1"
        mock_review.scorecard = None
        reviews = {"window_0": mock_review}

        result = {"existing": "data"}
        new_result = attach_attribution_to_walk_forward_result(result, reviews_by_window=reviews)

        self.assertIn("attribution_metadata", new_result)
        self.assertEqual(new_result["attribution_metadata"]["window_reviews"]["window_0"], "r_1")

    def test_attach_attribution_to_walk_forward_result_negative_oos(self):
        mock_review = MagicMock()
        mock_review.review_id = "r_1"
        mock_review.scorecard.total_net_pnl_usd = -100.0

        mock_review2 = MagicMock()
        mock_review2.review_id = "r_2"
        mock_review2.scorecard.total_net_pnl_usd = 100.0

        reviews = {"window_0": mock_review, "window_1": mock_review2}

        result = {"existing": "data"}
        new_result = attach_attribution_to_walk_forward_result(result, reviews_by_window=reviews)

        self.assertIn("warnings", new_result)
        self.assertEqual(len(new_result["warnings"]), 1)
        self.assertEqual(new_result["warnings"][0], "OOS window window_0 has negative contributor")

    def test_walk_forward_attribution_summary(self):
        result = {"attribution_metadata": {"summary": "data"}}
        summary = walk_forward_attribution_summary(result)
        self.assertEqual(summary, {"summary": "data"})

        self.assertEqual(walk_forward_attribution_summary({}), {})

    def test_walk_forward_attribution_warnings(self):
        result = {"warnings": ["warning1"]}
        warnings = walk_forward_attribution_warnings(result)
        self.assertEqual(warnings, ["warning1"])

        self.assertEqual(walk_forward_attribution_warnings({}), [])

if __name__ == "__main__":
    unittest.main()
