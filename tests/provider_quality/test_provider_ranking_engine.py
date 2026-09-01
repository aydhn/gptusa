import unittest
from unittest.mock import patch, MagicMock

from usa_signal_bot.provider_quality.phase109_models import ProviderSelectionScore, ProviderRanking
from usa_signal_bot.provider_quality.provider_ranking_engine import (
    assign_provider_ranks,
    rank_providers_for_symbol,
    provider_ranking_summary,
    provider_ranking_to_text
)

class TestProviderRankingEngine(unittest.TestCase):
    def setUp(self):
        self.mock_score_1 = MagicMock(spec=ProviderSelectionScore)
        self.mock_score_1.provider_name = "Provider A"
        self.mock_score_1.blocked = False
        self.mock_score_1.final_selection_score = 90.0
        self.mock_score_1.rank = None
        self.mock_score_1.risk_flags = ["FLAG_1"]

        self.mock_score_2 = MagicMock(spec=ProviderSelectionScore)
        self.mock_score_2.provider_name = "Provider B"
        self.mock_score_2.blocked = False
        self.mock_score_2.final_selection_score = 80.0
        self.mock_score_2.rank = None
        self.mock_score_2.risk_flags = ["FLAG_2"]

        self.mock_score_3 = MagicMock(spec=ProviderSelectionScore)
        self.mock_score_3.provider_name = "Provider Blocked"
        self.mock_score_3.blocked = True
        self.mock_score_3.final_selection_score = 95.0
        self.mock_score_3.rank = None
        self.mock_score_3.risk_flags = ["FLAG_3"]

    def test_assign_provider_ranks(self):
        scores = [self.mock_score_1, self.mock_score_2, self.mock_score_3]
        result = assign_provider_ranks(scores)
        self.assertEqual(len(result), 3)
        self.assertEqual(self.mock_score_1.rank, 1)
        self.assertEqual(self.mock_score_2.rank, 2)
        self.assertIsNone(self.mock_score_3.rank)

    def test_assign_provider_ranks_empty(self):
        self.assertEqual(assign_provider_ranks([]), [])

    def test_assign_provider_ranks_all_blocked(self):
        scores = [self.mock_score_3]
        result = assign_provider_ranks(scores)
        self.assertEqual(len(result), 1)
        self.assertIsNone(self.mock_score_3.rank)

    @patch("usa_signal_bot.provider_quality.provider_ranking_engine.datetime")
    @patch("usa_signal_bot.provider_quality.provider_ranking_engine.create_provider_ranking_id")
    def test_rank_providers_for_symbol(self, mock_create_id, mock_datetime):
        mock_create_id.return_value = "ranking_123"
        mock_datetime.datetime.utcnow.return_value.isoformat.return_value = "2023-01-01T00:00:00"

        scores = [self.mock_score_2, self.mock_score_1, self.mock_score_3]
        result = rank_providers_for_symbol("AAPL", "PRICE", scores)

        self.assertEqual(result.ranking_id, "ranking_123")
        self.assertEqual(result.created_at_utc, "2023-01-01T00:00:00Z")
        self.assertEqual(result.symbol, "AAPL")
        self.assertEqual(result.capability, "PRICE")
        self.assertEqual(len(result.scores), 3)
        self.assertTrue(result.scores[-1].blocked)
        self.assertEqual(result.ranked_provider_names, ["Provider A", "Provider B"])
        self.assertEqual(result.preferred_provider, "Provider A")
        self.assertEqual(result.fallback_providers, ["Provider B"])
        self.assertEqual(result.blocked_providers, ["Provider Blocked"])
        self.assertTrue(result.ranking_valid)
        self.assertTrue(result.ranking_is_research_data_only)
        self.assertFalse(result.produces_trade_signal)
        self.assertFalse(result.produces_order_decision)
        self.assertEqual(set(result.risk_flags), {"FLAG_1", "FLAG_2", "FLAG_3"})
        self.assertEqual(result.warnings, [])

    @patch("usa_signal_bot.provider_quality.provider_ranking_engine.datetime")
    @patch("usa_signal_bot.provider_quality.provider_ranking_engine.create_provider_ranking_id")
    def test_rank_providers_for_symbol_all_blocked(self, mock_create_id, mock_datetime):
        mock_create_id.return_value = "ranking_123"
        mock_datetime.datetime.utcnow.return_value.isoformat.return_value = "2023-01-01T00:00:00"

        scores = [self.mock_score_3]
        result = rank_providers_for_symbol("AAPL", "PRICE", scores)

        self.assertEqual(result.ranked_provider_names, [])
        self.assertIsNone(result.preferred_provider)
        self.assertEqual(result.fallback_providers, [])
        self.assertEqual(result.blocked_providers, ["Provider Blocked"])
        self.assertEqual(result.warnings, ["No selectable providers available."])

    def test_provider_ranking_summary(self):
        ranking = MagicMock(spec=ProviderRanking)
        ranking.ranking_id = "r_123"
        ranking.symbol = "AAPL"
        ranking.preferred_provider = "ProvA"
        ranking.fallback_providers = ["ProvB"]
        ranking.blocked_providers = ["ProvC"]

        summary = provider_ranking_summary(ranking)
        self.assertEqual(summary, {
            "ranking_id": "r_123",
            "symbol": "AAPL",
            "preferred": "ProvA",
            "fallbacks": ["ProvB"],
            "blocked": ["ProvC"]
        })

    def test_provider_ranking_to_text(self):
        ranking = MagicMock(spec=ProviderRanking)
        ranking.symbol = "AAPL"
        ranking.preferred_provider = "ProvA"
        ranking.fallback_providers = ["ProvB"]
        ranking.blocked_providers = ["ProvC"]

        text = provider_ranking_to_text(ranking)
        expected_text = "Provider Ranking | Symbol: AAPL\nPreferred: ProvA\nFallbacks: ProvB\nBlocked: ProvC"
        self.assertEqual(text, expected_text)

if __name__ == '__main__':
    unittest.main()
