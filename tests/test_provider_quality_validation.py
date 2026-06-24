import unittest
from usa_signal_bot.provider_quality.provider_quality_validation import (
    ProviderQualityValidationReport,
    assert_provider_quality_validation_valid
)
from usa_signal_bot.core.exceptions import ProviderQualityValidationError

class TestProviderQualityValidation(unittest.TestCase):
    def test_assert_provider_quality_validation_valid_passes(self):
        report = ProviderQualityValidationReport(
            valid=True,
            issue_count=0,
            warning_count=0,
            error_count=0,
            blocked_count=0,
            issues=[],
            warnings=[],
            errors=[]
        )
        # Should not raise any exception
        assert_provider_quality_validation_valid(report)

    def test_assert_provider_quality_validation_valid_raises(self):
        report = ProviderQualityValidationReport(
            valid=False,
            issue_count=1,
            warning_count=0,
            error_count=1,
            blocked_count=1,
            issues=[],
            warnings=[],
            errors=["Mock error message"]
        )

        with self.assertRaises(ProviderQualityValidationError) as context:
            assert_provider_quality_validation_valid(report)

        self.assertIn("Provider Quality Validation failed with 1 errors", str(context.exception))
        self.assertIn("Mock error message", str(context.exception))

if __name__ == "__main__":
    unittest.main()
