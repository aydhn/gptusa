import unittest
from unittest.mock import patch, MagicMock

import sys


# Provide mock for enums if missing
class CatchAllMockEnum:
    def __init__(self, value=""):
        self.value = value

    def __getattr__(self, name):
        return CatchAllMockEnum(name)


if "usa_signal_bot.core.enums" not in sys.modules:
    sys.modules["usa_signal_bot.core.enums"] = CatchAllMockEnum()


if "pandas" not in sys.modules:
    sys.modules["pandas"] = MagicMock()
if "yfinance" not in sys.modules:
    sys.modules["yfinance"] = MagicMock()
if "pytest" not in sys.modules:
    sys.modules["pytest"] = MagicMock()


class ProviderQualityValidationError(Exception):
    pass


if "usa_signal_bot.core.exceptions" not in sys.modules:

    class MockExceptions:
        ProviderQualityValidationError = ProviderQualityValidationError

    sys.modules["usa_signal_bot.core.exceptions"] = MockExceptions()
else:
    sys.modules["usa_signal_bot.core.exceptions"].ProviderQualityValidationError = (
        ProviderQualityValidationError
    )

from usa_signal_bot.provider_quality.freshness_scorer import (
    score_freshness,
    FreshnessParameters,
    _evaluate_freshness_status,
)


class TestFreshnessScorer(unittest.TestCase):

    def test_evaluate_freshness_status_expired(self):
        params = FreshnessParameters(fresh=False, stale=False, expired=True)
        score, warnings, flags = _evaluate_freshness_status(params)
        self.assertEqual(score, 0.0)
        self.assertEqual(warnings, ["Data is expired"])

    def test_evaluate_freshness_status_stale(self):
        params = FreshnessParameters(fresh=False, stale=True, expired=False)
        score, warnings, flags = _evaluate_freshness_status(params)
        self.assertEqual(score, 40.0)
        self.assertEqual(warnings, ["Data is stale"])

    def test_evaluate_freshness_status_fresh(self):
        params = FreshnessParameters(fresh=True, stale=False, expired=False)
        score, warnings, flags = _evaluate_freshness_status(params)
        self.assertEqual(score, 100.0)
        self.assertEqual(warnings, [])

    def test_evaluate_freshness_status_age(self):
        params = FreshnessParameters(
            fresh=False, stale=False, expired=False, age_seconds=50, ttl_seconds=100
        )
        score, warnings, flags = _evaluate_freshness_status(params)
        self.assertEqual(score, 75.0)
        self.assertEqual(warnings, [])

    def test_evaluate_freshness_status_age_old(self):
        params = FreshnessParameters(
            fresh=False, stale=False, expired=False, age_seconds=150, ttl_seconds=100
        )
        score, warnings, flags = _evaluate_freshness_status(params)
        self.assertEqual(score, 35.0)
        self.assertEqual(warnings, ["Data is relatively old"])

    @patch(
        "usa_signal_bot.provider_quality.freshness_scorer.create_data_quality_component_id"
    )
    @patch("usa_signal_bot.provider_quality.freshness_scorer.datetime")
    def test_score_freshness(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "test_id"
        mock_datetime.datetime.utcnow.return_value = MagicMock(
            isoformat=lambda: "2023-01-01T00:00:00"
        )

        params = FreshnessParameters(
            fresh=True, stale=False, expired=False, age_seconds=10, ttl_seconds=100
        )
        result = score_freshness(params, provider_name="TEST_PROV", symbol="BTC")

        self.assertEqual(result.score, 100.0)
        self.assertEqual(result.provider_name, "TEST_PROV")
        self.assertEqual(result.symbol, "BTC")
        self.assertEqual(result.raw_value, 10.0)
        self.assertIn("fresh=True", result.explanation)


if __name__ == "__main__":
    unittest.main()
