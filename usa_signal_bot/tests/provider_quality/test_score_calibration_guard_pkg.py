import unittest
from unittest.mock import MagicMock
from usa_signal_bot.provider_quality.score_calibration_guard import (
    validate_score_range,
    validate_component_weights,
    validate_quality_score_calibration,
    validate_selection_score_calibration,
    score_calibration_guard_summary,
    score_calibration_guard_to_text
)
from usa_signal_bot.provider_quality.phase109_models import (
    ProviderDataQualityScore,
    DataQualityScoreComponent,
    ProviderSelectionScore
)

class TestScoreCalibrationGuard(unittest.TestCase):
    def test_validate_score_range(self):
        self.assertEqual(validate_score_range(50.0), [])
        self.assertEqual(validate_score_range(0.0), [])
        self.assertEqual(validate_score_range(100.0), [])
        self.assertEqual(validate_score_range(None), [])
        self.assertEqual(validate_score_range(-1.0), ["score must be between 0 and 100, got -1.0"])
        self.assertEqual(validate_score_range(101.0, "custom"), ["custom must be between 0 and 100, got 101.0"])

    def test_validate_component_weights(self):
        comp1 = MagicMock()
        comp1.weight = 0.5
        comp2 = MagicMock()
        comp2.weight = 0.5
        self.assertEqual(validate_component_weights([comp1, comp2]), [])

        comp3 = MagicMock()
        comp3.weight = 0.6
        self.assertEqual(validate_component_weights([comp1, comp3]), ["Component weights sum to 1.1, expected 1.0"])

        self.assertEqual(validate_component_weights([]), [])

    def test_validate_quality_score_calibration(self):
        comp1 = MagicMock()
        comp1.score = 80.0
        comp1.weight = 0.5
        comp1.weighted_score = 40.0
        comp1.component.value = "COMP1"

        comp2 = MagicMock()
        comp2.score = 90.0
        comp2.weight = 0.5
        comp2.weighted_score = 45.0
        comp2.component.value = "COMP2"

        score = MagicMock()
        score.total_score = 85.0
        score.components = [comp1, comp2]

        self.assertEqual(validate_quality_score_calibration(score), [])

        score.total_score = -5.0
        self.assertIn("total_score must be between 0 and 100, got -5.0", validate_quality_score_calibration(score))
        score.total_score = 85.0

        comp1.weighted_score = 85.0
        self.assertIn("Weighted score 85.0 exceeds base score 80.0 for COMP1", validate_quality_score_calibration(score))
        comp1.weighted_score = 40.0

        comp1.score = -10.0
        self.assertIn("component COMP1 score must be between 0 and 100, got -10.0", validate_quality_score_calibration(score))

    def test_validate_selection_score_calibration(self):
        score = MagicMock()
        score.final_selection_score = 80.0
        score.quality_score = 80.0
        score.trust_score = 80.0
        score.freshness_score = 80.0
        score.safety_score = 80.0
        score.availability_score = 80.0

        self.assertEqual(validate_selection_score_calibration(score), [])

        score.final_selection_score = 105.0
        self.assertIn("final_selection_score must be between 0 and 100, got 105.0", validate_selection_score_calibration(score))

    def test_score_calibration_guard_summary(self):
        self.assertEqual(score_calibration_guard_summary([]), {"valid": True, "error_count": 0, "errors": []})
        errors = ["error 1", "error 2"]
        self.assertEqual(score_calibration_guard_summary(errors), {"valid": False, "error_count": 2, "errors": errors})

    def test_score_calibration_guard_to_text(self):
        self.assertEqual(score_calibration_guard_to_text([]), "Score Calibration Guard: PASSED")
        errors = ["error 1", "error 2"]
        self.assertEqual(score_calibration_guard_to_text(errors), "Score Calibration Guard: FAILED\n  error 1\n  error 2")

if __name__ == "__main__":
    unittest.main()
