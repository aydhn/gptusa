import sys
import unittest
from unittest.mock import patch, MagicMock

# We define CatchAllMockEnum, but we DON'T override sys.modules at import time.
class CatchAllMockEnum:
    def __init__(self, value=""):
        self._value = str(value)
    def __getattr__(self, name):
        if name in ('__iter__', '__bases__', '__mro__', '__class__'):
            raise AttributeError
        return CatchAllMockEnum(name)
    def __call__(self, *args, **kwargs):
        return self
    def __hash__(self):
        return hash(self._value)
    def __eq__(self, other):
        if isinstance(other, CatchAllMockEnum):
            return self._value == other._value
        return str(self) == str(other)
    def __str__(self):
        return self._value
    def __or__(self, other):
        return self
    def __ror__(self, other):
        return self
    @property
    def value(self):
        return self._value
    def __deepcopy__(self, memo):
        return self

class TestScoreCalibrationGuard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.patcher = patch.dict(sys.modules, {'usa_signal_bot.core.enums': CatchAllMockEnum()})
        cls.patcher.start()

        # We must import inside the test/setup after mocking
        global validate_score_range, validate_component_weights, validate_quality_score_calibration
        global validate_selection_score_calibration, score_calibration_guard_summary, score_calibration_guard_to_text
        global ProviderDataQualityScore, DataQualityScoreComponent, ProviderSelectionScore

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

    @classmethod
    def tearDownClass(cls):
        cls.patcher.stop()

    def test_validate_score_range(self):
        self.assertEqual(validate_score_range(None), [])
        self.assertEqual(validate_score_range(50.0), [])
        self.assertEqual(validate_score_range(100.0), [])
        self.assertEqual(validate_score_range(0.0), [])

        errors = validate_score_range(-1.0)
        self.assertEqual(len(errors), 1)
        self.assertIn("-1.0", errors[0])

        errors = validate_score_range(100.1, "my_field")
        self.assertEqual(len(errors), 1)
        self.assertIn("my_field", errors[0])
        self.assertIn("100.1", errors[0])

    def test_validate_component_weights(self):
        self.assertEqual(validate_component_weights([]), [])

        c1 = DataQualityScoreComponent(weight=0.5, score=100.0, weighted_score=50.0, component_id="1", created_at_utc="", provider_name="", symbol="", component=CatchAllMockEnum("test"), raw_value=0.0, grade=CatchAllMockEnum("test"), explanation="")
        c2 = DataQualityScoreComponent(weight=0.5, score=100.0, weighted_score=50.0, component_id="2", created_at_utc="", provider_name="", symbol="", component=CatchAllMockEnum("test"), raw_value=0.0, grade=CatchAllMockEnum("test"), explanation="")
        self.assertEqual(validate_component_weights([c1, c2]), [])

        c3 = DataQualityScoreComponent(weight=0.6, score=100.0, weighted_score=60.0, component_id="3", created_at_utc="", provider_name="", symbol="", component=CatchAllMockEnum("test"), raw_value=0.0, grade=CatchAllMockEnum("test"), explanation="")
        errors = validate_component_weights([c1, c3])
        self.assertEqual(len(errors), 1)
        self.assertIn("expected 1.0", errors[0])

    def test_validate_quality_score_calibration(self):
        c1 = DataQualityScoreComponent(weight=1.0, score=80.0, weighted_score=80.0, component_id="1", created_at_utc="", provider_name="", symbol="", component=CatchAllMockEnum("test1"), raw_value=0.0, grade=CatchAllMockEnum("test"), explanation="")
        score = ProviderDataQualityScore(total_score=80.0, components=[c1], score_id="1", created_at_utc="", provider_name="", symbol="", capability="", grade=CatchAllMockEnum("test"), usable_for_research=True, use_with_warning=False, blocked=False, explanation="")

        errors = validate_quality_score_calibration(score)
        self.assertEqual(errors, [])

        c2 = DataQualityScoreComponent(weight=1.0, score=80.0, weighted_score=85.0, component_id="2", created_at_utc="", provider_name="", symbol="", component=CatchAllMockEnum("test2"), raw_value=0.0, grade=CatchAllMockEnum("test"), explanation="")
        score2 = ProviderDataQualityScore(total_score=105.0, components=[c2], score_id="2", created_at_utc="", provider_name="", symbol="", capability="", grade=CatchAllMockEnum("test"), usable_for_research=True, use_with_warning=False, blocked=False, explanation="")

        errors2 = validate_quality_score_calibration(score2)
        self.assertEqual(len(errors2), 2)
        self.assertIn("total_score must be between 0 and 100", errors2[0])
        self.assertIn("Weighted score 85.0 exceeds base score 80.0", errors2[1])

    def test_validate_selection_score_calibration(self):
        score = ProviderSelectionScore(
            final_selection_score=85.0,
            quality_score=90.0,
            trust_score=80.0,
            freshness_score=95.0,
            safety_score=100.0,
            availability_score=75.0,
            selection_score_id="1", created_at_utc="", provider_name="", symbol="", capability="", data_quality_score_id="", trust_profile_id="", status=CatchAllMockEnum("test"), decision=CatchAllMockEnum("test"), rank=1, selectable_for_research=True, use_as_fallback=False, blocked=False, explanation=""
        )
        self.assertEqual(validate_selection_score_calibration(score), [])

        score.final_selection_score = -5.0
        score.trust_score = 110.0
        errors = validate_selection_score_calibration(score)
        self.assertEqual(len(errors), 2)
        self.assertIn("final_selection_score", errors[0])
        self.assertIn("trust_score", errors[1])

    def test_score_calibration_guard_summary(self):
        summary1 = score_calibration_guard_summary([])
        self.assertTrue(summary1["valid"])
        self.assertEqual(summary1["error_count"], 0)

        summary2 = score_calibration_guard_summary(["error1"])
        self.assertFalse(summary2["valid"])
        self.assertEqual(summary2["error_count"], 1)

    def test_score_calibration_guard_to_text(self):
        self.assertEqual(score_calibration_guard_to_text([]), "Score Calibration Guard: PASSED")

        text = score_calibration_guard_to_text(["error1", "error2"])
        self.assertTrue(text.startswith("Score Calibration Guard: FAILED"))
        self.assertIn("error1", text)
        self.assertIn("error2", text)

if __name__ == '__main__':
    unittest.main()
