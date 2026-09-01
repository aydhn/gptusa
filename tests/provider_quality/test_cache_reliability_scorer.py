import unittest
from unittest.mock import patch, MagicMock

from usa_signal_bot.provider_quality.cache_reliability_scorer import (
    cache_reliability_grade,
    cache_reliability_score_from_status,
    score_cache_reliability,
    cache_reliability_scorer_to_text,
)

from usa_signal_bot.core.enums import (
    DataQualityGrade,
    ProviderQualityRiskFlag,
    DataQualityComponent,
)

class TestCacheReliabilityScorer(unittest.TestCase):

    def test_cache_reliability_grade(self):
        self.assertEqual(cache_reliability_grade(100), DataQualityGrade.EXCELLENT)
        self.assertEqual(cache_reliability_grade(90), DataQualityGrade.EXCELLENT)
        self.assertEqual(cache_reliability_grade(89.9), DataQualityGrade.GOOD)
        self.assertEqual(cache_reliability_grade(70), DataQualityGrade.GOOD)
        self.assertEqual(cache_reliability_grade(69.9), DataQualityGrade.ACCEPTABLE)
        self.assertEqual(cache_reliability_grade(50), DataQualityGrade.ACCEPTABLE)
        self.assertEqual(cache_reliability_grade(49.9), DataQualityGrade.WEAK)
        self.assertEqual(cache_reliability_grade(30), DataQualityGrade.WEAK)
        self.assertEqual(cache_reliability_grade(29.9), DataQualityGrade.POOR)
        self.assertEqual(cache_reliability_grade(0), DataQualityGrade.POOR)
        self.assertEqual(cache_reliability_grade(-1), DataQualityGrade.POOR)

    def test_cache_reliability_score_from_status(self):
        # Happy path
        self.assertEqual(cache_reliability_score_from_status("VALID", True, True), 100.0)
        self.assertEqual(cache_reliability_score_from_status(None, True, True), 100.0)

        # Missing or corrupt
        self.assertEqual(cache_reliability_score_from_status("MISSING", True, True), 0.0)
        self.assertEqual(cache_reliability_score_from_status("CACHE_MISS", True, True), 0.0)
        self.assertEqual(cache_reliability_score_from_status("CORRUPT", True, True), 0.0)

        # Stale
        self.assertEqual(cache_reliability_score_from_status("STALE", True, True), 80.0)

        # Missing checksum
        self.assertEqual(cache_reliability_score_from_status("VALID", False, True), 90.0)

        # Invalid schema
        self.assertEqual(cache_reliability_score_from_status("VALID", True, False), 50.0)

        # Combinations
        self.assertEqual(cache_reliability_score_from_status("STALE", False, True), 70.0)
        self.assertEqual(cache_reliability_score_from_status("STALE", True, False), 30.0)
        self.assertEqual(cache_reliability_score_from_status("STALE", False, False), 20.0)

        # Floor at 0
        self.assertEqual(cache_reliability_score_from_status("MISSING", False, False), 0.0)

    @patch("usa_signal_bot.provider_quality.cache_reliability_scorer.create_data_quality_component_id")
    @patch("usa_signal_bot.provider_quality.cache_reliability_scorer.datetime")
    def test_score_cache_reliability_perfect(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "comp_cache_1"
        mock_datetime.datetime.utcnow.return_value = MagicMock(
            isoformat=lambda: "2023-01-01T00:00:00"
        )

        result = score_cache_reliability("VALID", checksum_present=True, schema_valid=True, provider_name="PROV1", symbol="AAPL")

        self.assertEqual(result.component_id, "comp_cache_1")
        self.assertEqual(result.created_at_utc, "2023-01-01T00:00:00Z")
        self.assertEqual(result.provider_name, "PROV1")
        self.assertEqual(result.symbol, "AAPL")
        self.assertEqual(result.component, DataQualityComponent.CACHE_RELIABILITY)
        self.assertEqual(result.score, 100.0)
        self.assertEqual(result.grade, DataQualityGrade.EXCELLENT)
        self.assertEqual(result.risk_flags, [])
        self.assertEqual(result.warnings, [])

    @patch("usa_signal_bot.provider_quality.cache_reliability_scorer.create_data_quality_component_id")
    @patch("usa_signal_bot.provider_quality.cache_reliability_scorer.datetime")
    def test_score_cache_reliability_missing(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "comp_cache_2"
        mock_datetime.datetime.utcnow.return_value = MagicMock(
            isoformat=lambda: "2023-01-01T00:00:00"
        )

        result = score_cache_reliability("MISSING", checksum_present=True, schema_valid=True)

        self.assertEqual(result.score, 0.0)
        self.assertEqual(result.grade, DataQualityGrade.POOR)
        self.assertIn(ProviderQualityRiskFlag.PROVIDER_CACHE_MISSING, result.risk_flags)
        self.assertTrue(any("missing" in w.lower() for w in result.warnings))

    @patch("usa_signal_bot.provider_quality.cache_reliability_scorer.create_data_quality_component_id")
    @patch("usa_signal_bot.provider_quality.cache_reliability_scorer.datetime")
    def test_score_cache_reliability_invalid_schema(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "comp_cache_3"
        mock_datetime.datetime.utcnow.return_value = MagicMock(
            isoformat=lambda: "2023-01-01T00:00:00"
        )

        result = score_cache_reliability("VALID", checksum_present=True, schema_valid=False)

        self.assertEqual(result.score, 50.0)
        self.assertEqual(result.grade, DataQualityGrade.ACCEPTABLE)
        self.assertIn(ProviderQualityRiskFlag.PROVIDER_CACHE_INVALID, result.risk_flags)
        self.assertTrue(any("schema" in w.lower() for w in result.warnings))

    @patch("usa_signal_bot.provider_quality.cache_reliability_scorer.create_data_quality_component_id")
    @patch("usa_signal_bot.provider_quality.cache_reliability_scorer.datetime")
    def test_score_cache_reliability_missing_checksum(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "comp_cache_4"
        mock_datetime.datetime.utcnow.return_value = MagicMock(
            isoformat=lambda: "2023-01-01T00:00:00"
        )

        result = score_cache_reliability("VALID", checksum_present=False, schema_valid=True)

        self.assertEqual(result.score, 90.0)
        self.assertEqual(result.grade, DataQualityGrade.EXCELLENT)
        self.assertTrue(any("checksum" in w.lower() for w in result.warnings))

    @patch("usa_signal_bot.provider_quality.cache_reliability_scorer.create_data_quality_component_id")
    @patch("usa_signal_bot.provider_quality.cache_reliability_scorer.datetime")
    def test_cache_reliability_scorer_to_text(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "comp_cache_5"
        mock_datetime.datetime.utcnow.return_value = MagicMock(
            isoformat=lambda: "2023-01-01T00:00:00"
        )

        result = score_cache_reliability("VALID", checksum_present=True, schema_valid=True)
        text = cache_reliability_scorer_to_text(result)

        self.assertIn("Cache Reliability: 100.0", text)
        self.assertIn("EXCELLENT", text)
        self.assertIn("based on status VALID", text)

if __name__ == "__main__":
    unittest.main()
