import unittest
from unittest.mock import patch, MagicMock

# The wrapper will patch sys.modules if needed, but inside this permanent test
# file we should use standard imports where possible, or just expect the wrapper
# to have provided the missing modules before import time.

from usa_signal_bot.provider_quality.schema_validity_scorer import (
    schema_validity_grade,
    schema_validity_score_from_errors,
    score_schema_validity,
    schema_validity_scorer_to_text,
)

# If enums module is successfully loaded (or mocked properly), we can import DataQualityGrade
try:
    from usa_signal_bot.core.enums import (
        DataQualityGrade,
        ProviderQualityRiskFlag,
        DataQualityComponent,
    )
except ImportError:
    # If the standard import fails despite sys.modules patching (unlikely if patched correctly in wrapper),
    # define dummy fallback variables for types.
    class DummyEnum:
        def __init__(self, value):
            self.value = value
            self.name = value

    class DataQualityGrade:
        EXCELLENT = DummyEnum("EXCELLENT")
        ACCEPTABLE = DummyEnum("ACCEPTABLE")
        WEAK = DummyEnum("WEAK")
        POOR = DummyEnum("POOR")
        BLOCKED = DummyEnum("BLOCKED")

    class ProviderQualityRiskFlag:
        SCHEMA_INVALID = DummyEnum("SCHEMA_INVALID")

    class DataQualityComponent:
        SCHEMA_VALIDITY = DummyEnum("SCHEMA_VALIDITY")


class TestSchemaValidityScorer(unittest.TestCase):

    def test_schema_validity_grade(self):
        self.assertEqual(schema_validity_grade(100), DataQualityGrade.EXCELLENT)
        self.assertEqual(schema_validity_grade(99), DataQualityGrade.EXCELLENT)
        self.assertEqual(schema_validity_grade(98.9), DataQualityGrade.ACCEPTABLE)
        self.assertEqual(schema_validity_grade(80), DataQualityGrade.ACCEPTABLE)
        self.assertEqual(schema_validity_grade(79.9), DataQualityGrade.WEAK)
        self.assertEqual(schema_validity_grade(50), DataQualityGrade.WEAK)
        self.assertEqual(schema_validity_grade(49.9), DataQualityGrade.POOR)
        self.assertEqual(schema_validity_grade(0.1), DataQualityGrade.POOR)
        self.assertEqual(schema_validity_grade(0), DataQualityGrade.BLOCKED)
        self.assertEqual(schema_validity_grade(-1), DataQualityGrade.BLOCKED)

    def test_schema_validity_score_from_errors(self):
        self.assertEqual(schema_validity_score_from_errors([]), 100.0)
        self.assertEqual(schema_validity_score_from_errors(["error1"]), 80.0)
        self.assertEqual(schema_validity_score_from_errors(["error1", "error2"]), 60.0)
        self.assertEqual(schema_validity_score_from_errors(["err"] * 5), 0.0)
        self.assertEqual(schema_validity_score_from_errors(["err"] * 6), 0.0)

    @patch(
        "usa_signal_bot.provider_quality.schema_validity_scorer.create_data_quality_component_id"
    )
    @patch("usa_signal_bot.provider_quality.schema_validity_scorer.datetime")
    def test_score_schema_validity_no_errors(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "dq_comp_test1"
        mock_datetime.datetime.utcnow.return_value = MagicMock(
            isoformat=lambda: "2023-01-01T00:00:00"
        )

        result = score_schema_validity([], provider_name="TEST_PROV", symbol="BTC")

        self.assertEqual(result.component_id, "dq_comp_test1")
        self.assertEqual(result.created_at_utc, "2023-01-01T00:00:00Z")
        self.assertEqual(result.provider_name, "TEST_PROV")
        self.assertEqual(result.symbol, "BTC")
        self.assertEqual(result.component, DataQualityComponent.SCHEMA_VALIDITY)
        self.assertEqual(result.raw_value, 0.0)
        self.assertEqual(result.score, 100.0)
        self.assertEqual(result.weight, 0.0)
        self.assertEqual(result.weighted_score, 0.0)
        self.assertEqual(result.grade, DataQualityGrade.EXCELLENT)
        self.assertIn("100.0", result.explanation)
        self.assertIn("0 errors", result.explanation)
        self.assertEqual(result.risk_flags, [])
        self.assertEqual(result.warnings, [])

    @patch(
        "usa_signal_bot.provider_quality.schema_validity_scorer.create_data_quality_component_id"
    )
    @patch("usa_signal_bot.provider_quality.schema_validity_scorer.datetime")
    def test_score_schema_validity_with_errors(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "dq_comp_test2"
        mock_datetime.datetime.utcnow.return_value = MagicMock(
            isoformat=lambda: "2023-01-01T00:00:00"
        )

        errors = ["Missing field X", "Invalid type for Y"]
        result = score_schema_validity(errors, provider_name="TEST_PROV2")

        self.assertEqual(result.provider_name, "TEST_PROV2")
        self.assertEqual(result.raw_value, 2.0)
        self.assertEqual(result.score, 60.0)
        self.assertEqual(result.grade, DataQualityGrade.WEAK)
        self.assertIn("60.0", result.explanation)
        self.assertIn("2 errors", result.explanation)
        self.assertIn(ProviderQualityRiskFlag.SCHEMA_INVALID, result.risk_flags)
        self.assertEqual(result.warnings, errors)

    @patch(
        "usa_signal_bot.provider_quality.schema_validity_scorer.create_data_quality_component_id"
    )
    @patch("usa_signal_bot.provider_quality.schema_validity_scorer.datetime")
    def test_schema_validity_scorer_to_text(self, mock_datetime, mock_create_id):
        mock_create_id.return_value = "dq_comp_test3"
        mock_datetime.datetime.utcnow.return_value = MagicMock(
            isoformat=lambda: "2023-01-01T00:00:00"
        )

        result = score_schema_validity(["Error1"], provider_name="PROV")
        text = schema_validity_scorer_to_text(result)

        self.assertIn("Schema Validity: 80.0", text)
        self.assertIn("ACCEPTABLE", text)
        self.assertIn("Schema validity is 80.0 with 1 errors", text)


if __name__ == "__main__":
    unittest.main()
