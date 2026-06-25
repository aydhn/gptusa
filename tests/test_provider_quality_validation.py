import unittest
from unittest.mock import MagicMock

from usa_signal_bot.provider_quality.provider_quality_validation import (
    ProviderQualityValidationReport,
    ProviderQualityValidationIssue,
    assert_provider_quality_validation_valid,
    provider_quality_validation_report_to_text,
)
from usa_signal_bot.core.exceptions import ProviderQualityValidationError


class TestProviderQualityValidation(unittest.TestCase):
    def test_assert_provider_quality_validation_valid_success(self):
        report = ProviderQualityValidationReport(
            valid=True,
            issue_count=0,
            warning_count=0,
            error_count=0,
            blocked_count=0,
            issues=[],
            warnings=[],
            errors=[],
        )
        # Should not raise
        assert_provider_quality_validation_valid(report)

    def test_assert_provider_quality_validation_valid_failure(self):
        report = ProviderQualityValidationReport(
            valid=False,
            issue_count=1,
            warning_count=0,
            error_count=1,
            blocked_count=1,
            issues=[
                ProviderQualityValidationIssue("ERROR", "test_field", "test error")
            ],
            warnings=[],
            errors=["test error"],
        )
        with self.assertRaises(ProviderQualityValidationError) as context:
            assert_provider_quality_validation_valid(report)

        self.assertIn(
            "Provider Quality Validation failed with 1 errors", str(context.exception)
        )
        self.assertIn("['test error']", str(context.exception))

    def test_provider_quality_validation_report_to_text_valid(self):
        report = ProviderQualityValidationReport(
            valid=True,
            issue_count=0,
            warning_count=0,
            error_count=0,
            blocked_count=0,
            issues=[],
            warnings=[],
            errors=[],
        )
        result = provider_quality_validation_report_to_text(report)
        self.assertEqual(result, "Provider Quality Validation: PASSED")

    def test_provider_quality_validation_report_to_text_invalid(self):
        report = ProviderQualityValidationReport(
            valid=False,
            issue_count=2,
            warning_count=0,
            error_count=2,
            blocked_count=2,
            issues=[],
            warnings=[],
            errors=["Error 1", "Error 2"],
        )
        result = provider_quality_validation_report_to_text(report)
        self.assertEqual(
            result, "Provider Quality Validation: FAILED\n  Error 1\n  Error 2"
        )


if __name__ == "__main__":
    unittest.main()
