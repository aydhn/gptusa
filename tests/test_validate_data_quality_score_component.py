import unittest
from unittest.mock import MagicMock

# standard module imports
from usa_signal_bot.provider_quality.phase109_models import (
    validate_data_quality_score_component,
)
from usa_signal_bot.core.exceptions import ProviderQualityValidationError


class TestValidateDataQualityScoreComponent(unittest.TestCase):

    def test_happy_path_valid_scores(self):
        item = MagicMock()
        item.score = 50.0
        item.weight = 0.5
        # Should not raise an exception
        validate_data_quality_score_component(item)

    def test_edge_case_zero_score_zero_weight(self):
        item = MagicMock()
        item.score = 0.0
        item.weight = 0.0
        # Should not raise an exception
        validate_data_quality_score_component(item)

    def test_edge_case_max_score_max_weight(self):
        item = MagicMock()
        item.score = 100.0
        item.weight = 1.0
        # Should not raise an exception
        validate_data_quality_score_component(item)

    def test_validation_fails_when_score_less_than_zero(self):
        item = MagicMock()
        item.score = -0.1
        item.weight = 0.5
        with self.assertRaisesRegex(
            ProviderQualityValidationError, "Score must be between 0 and 100"
        ):
            validate_data_quality_score_component(item)

    def test_validation_fails_when_score_greater_than_100(self):
        item = MagicMock()
        item.score = 100.1
        item.weight = 0.5
        with self.assertRaisesRegex(
            ProviderQualityValidationError, "Score must be between 0 and 100"
        ):
            validate_data_quality_score_component(item)

    def test_validation_fails_when_weight_less_than_zero(self):
        item = MagicMock()
        item.score = 50.0
        item.weight = -0.01
        with self.assertRaisesRegex(
            ProviderQualityValidationError, "Weight must be between 0 and 1.0"
        ):
            validate_data_quality_score_component(item)

    def test_validation_fails_when_weight_greater_than_one(self):
        item = MagicMock()
        item.score = 50.0
        item.weight = 1.01
        with self.assertRaisesRegex(
            ProviderQualityValidationError, "Weight must be between 0 and 1.0"
        ):
            validate_data_quality_score_component(item)


if __name__ == "__main__":
    unittest.main()
