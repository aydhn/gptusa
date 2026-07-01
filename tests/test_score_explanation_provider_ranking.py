import unittest
from unittest.mock import MagicMock, patch
from usa_signal_bot.provider_quality.score_explanation import explain_provider_ranking

class TestExplainProviderRanking(unittest.TestCase):
    @patch('usa_signal_bot.provider_quality.score_explanation.score_explanation_safety_check')
    def test_explain_provider_ranking_success(self, mock_safety_check):
        mock_safety_check.return_value = []

        ranking = MagicMock()
        ranking.symbol = "AAPL"
        ranking.preferred_provider = "AlphaVantage"
        ranking.fallback_providers = ["Yahoo", "Polygon"]
        ranking.blocked_providers = ["ShadySource"]

        result = explain_provider_ranking(ranking)

        self.assertIn("Provider Ranking for AAPL is prepared strictly for research data sourcing.", result)
        self.assertIn("Preferred data source: AlphaVantage.", result)
        self.assertIn("Available fallbacks: Yahoo, Polygon.", result)
        self.assertIn("Blocked sources: ShadySource.", result)
        self.assertIn("Notice: This ranking does not produce trade signals or execution orders.", result)

    @patch('usa_signal_bot.provider_quality.score_explanation.score_explanation_safety_check')
    def test_explain_provider_ranking_missing_fields(self, mock_safety_check):
        mock_safety_check.return_value = []

        ranking = MagicMock()
        ranking.symbol = "AAPL"
        ranking.preferred_provider = None
        ranking.fallback_providers = []
        ranking.blocked_providers = []

        result = explain_provider_ranking(ranking)

        self.assertIn("Provider Ranking for AAPL is prepared strictly for research data sourcing.", result)
        self.assertNotIn("Preferred data source", result)
        self.assertNotIn("Available fallbacks", result)
        self.assertNotIn("Blocked sources", result)
        self.assertIn("Notice: This ranking does not produce trade signals or execution orders.", result)

    @patch('usa_signal_bot.provider_quality.score_explanation.score_explanation_safety_check')
    def test_explain_provider_ranking_unsafe_term(self, mock_safety_check):
        mock_safety_check.return_value = ["Unsafe term detected"]

        ranking = MagicMock()
        ranking.symbol = "AAPL"
        ranking.preferred_provider = "AlphaVantage"
        ranking.fallback_providers = ["PortfolioMaker"]
        ranking.blocked_providers = []

        result = explain_provider_ranking(ranking)

        self.assertEqual(result, "Explanation blocked due to unsafe language.")
