import unittest
from usa_signal_bot.provider_quality.schema_validity_scorer import (
    score_schema_validity,
    schema_validity_grade,
    schema_validity_score_from_errors,
    schema_validity_scorer_to_text
)

class TestSchemaValidityScorer(unittest.TestCase):
    def test_schema_validity_grade(self):
        self.assertEqual(schema_validity_grade(100.0).value, "EXCELLENT")
        self.assertEqual(schema_validity_grade(99.0).value, "EXCELLENT")
        self.assertEqual(schema_validity_grade(85.0).value, "ACCEPTABLE")
        self.assertEqual(schema_validity_grade(80.0).value, "ACCEPTABLE")
        self.assertEqual(schema_validity_grade(60.0).value, "WEAK")
        self.assertEqual(schema_validity_grade(50.0).value, "WEAK")
        self.assertEqual(schema_validity_grade(25.0).value, "POOR")
        self.assertEqual(schema_validity_grade(1.0).value, "POOR")
        self.assertEqual(schema_validity_grade(0.0).value, "BLOCKED")
        self.assertEqual(schema_validity_grade(-10.0).value, "BLOCKED")

    def test_schema_validity_score_from_errors(self):
        self.assertEqual(schema_validity_score_from_errors([]), 100.0)
        self.assertEqual(schema_validity_score_from_errors(["error1"]), 80.0)
        self.assertEqual(schema_validity_score_from_errors(["error1", "error2"]), 60.0)
        self.assertEqual(schema_validity_score_from_errors(["error1", "error2", "error3", "error4", "error5"]), 0.0)
        self.assertEqual(schema_validity_score_from_errors(["error1", "error2", "error3", "error4", "error5", "error6"]), 0.0)

    def test_score_schema_validity_no_errors(self):
        result = score_schema_validity([], provider_name="TEST_PROVIDER", symbol="TEST_SYMBOL")
        self.assertEqual(result.provider_name, "TEST_PROVIDER")
        self.assertEqual(result.symbol, "TEST_SYMBOL")
        self.assertEqual(result.score, 100.0)
        self.assertEqual(result.raw_value, 0.0)
        self.assertEqual(result.grade.value, "EXCELLENT")
        self.assertEqual(result.risk_flags, [])
        self.assertEqual(result.warnings, [])
        self.assertTrue(result.created_at_utc.endswith("Z"))

    def test_score_schema_validity_with_errors(self):
        errors = ["Missing field X", "Invalid type for Y"]
        result = score_schema_validity(errors, provider_name="TEST_PROVIDER", symbol="TEST_SYMBOL")
        self.assertEqual(result.provider_name, "TEST_PROVIDER")
        self.assertEqual(result.symbol, "TEST_SYMBOL")
        self.assertEqual(result.score, 60.0)
        self.assertEqual(result.raw_value, 2.0)
        self.assertEqual(result.grade.value, "WEAK")
        self.assertEqual(len(result.risk_flags), 1)
        self.assertEqual(result.risk_flags[0].value, "SCHEMA_INVALID")
        self.assertEqual(result.warnings, errors)

    def test_schema_validity_scorer_to_text(self):
        result = score_schema_validity(["error"], provider_name="TEST_PROVIDER", symbol="TEST_SYMBOL")
        text = schema_validity_scorer_to_text(result)
        self.assertTrue(text.startswith("Schema Validity: 80.0"))
        self.assertTrue("ACCEPTABLE" in text)
        self.assertTrue("1 errors" in text)
