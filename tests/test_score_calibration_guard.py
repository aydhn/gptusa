import pytest
from unittest.mock import MagicMock, patch
import sys

class CatchAllMockException(Exception): pass
class MockExceptions:
    def __getattr__(self, name): return CatchAllMockException

with patch.dict('sys.modules', {'usa_signal_bot.core.enums': MagicMock()}):
    from usa_signal_bot.provider_quality.phase109_models import (
        ProviderDataQualityScore,
        DataQualityScoreComponent,
        ProviderSelectionScore
    )
    from usa_signal_bot.provider_quality.score_calibration_guard import (
        validate_score_range,
        validate_component_weights,
        validate_quality_score_calibration,
        validate_selection_score_calibration,
        score_calibration_guard_summary,
        score_calibration_guard_to_text
    )

def test_validate_score_range():
    assert validate_score_range(None) == []
    assert validate_score_range(50.0) == []
    assert validate_score_range(0.0) == []
    assert validate_score_range(100.0) == []
    assert validate_score_range(-1.0) == ["score must be between 0 and 100, got -1.0"]
    assert validate_score_range(101.0, "test_field") == ["test_field must be between 0 and 100, got 101.0"]

def test_validate_component_weights():
    c1 = MagicMock(spec=DataQualityScoreComponent)
    c1.weight = 0.5
    c2 = MagicMock(spec=DataQualityScoreComponent)
    c2.weight = 0.5
    assert validate_component_weights([c1, c2]) == []

    c3 = MagicMock(spec=DataQualityScoreComponent)
    c3.weight = 0.6
    assert validate_component_weights([c1, c3]) == ["Component weights sum to 1.1, expected 1.0"]

    c4 = MagicMock(spec=DataQualityScoreComponent)
    c4.weight = 0.0
    assert validate_component_weights([c4]) == []

    assert validate_component_weights([]) == []

def test_validate_quality_score_calibration():
    score = MagicMock(spec=ProviderDataQualityScore)
    score.total_score = 50.0

    comp1 = MagicMock(spec=DataQualityScoreComponent)
    comp1.score = 60.0
    comp1.weighted_score = 30.0
    comp1.weight = 0.5
    comp1.component = MagicMock()
    comp1.component.value = "comp1"

    comp2 = MagicMock(spec=DataQualityScoreComponent)
    comp2.score = 40.0
    comp2.weighted_score = 20.0
    comp2.weight = 0.5
    comp2.component = MagicMock()
    comp2.component.value = "comp2"

    score.components = [comp1, comp2]
    assert validate_quality_score_calibration(score) == []

    score.total_score = 110.0
    comp1.weighted_score = 70.0
    comp1.weight = 0.6

    errors = validate_quality_score_calibration(score)
    assert len(errors) == 3
    assert "total_score must be between 0 and 100, got 110.0" in errors
    assert "Weighted score 70.0 exceeds base score 60.0 for comp1" in errors
    assert "Component weights sum to 1.1, expected 1.0" in errors

def test_validate_selection_score_calibration():
    score = MagicMock(spec=ProviderSelectionScore)
    score.final_selection_score = 80.0
    score.quality_score = 90.0
    score.trust_score = 70.0
    score.freshness_score = 85.0
    score.safety_score = 95.0
    score.availability_score = 100.0

    assert validate_selection_score_calibration(score) == []

    score.final_selection_score = -5.0
    score.safety_score = 105.0

    errors = validate_selection_score_calibration(score)
    assert len(errors) == 2
    assert "final_selection_score must be between 0 and 100, got -5.0" in errors
    assert "safety_score must be between 0 and 100, got 105.0" in errors

def test_score_calibration_guard_summary():
    assert score_calibration_guard_summary([]) == {"valid": True, "error_count": 0, "errors": []}
    assert score_calibration_guard_summary(["error1", "error2"]) == {"valid": False, "error_count": 2, "errors": ["error1", "error2"]}

def test_score_calibration_guard_to_text():
    assert score_calibration_guard_to_text([]) == "Score Calibration Guard: PASSED"
    assert score_calibration_guard_to_text(["error1", "error2"]) == "Score Calibration Guard: FAILED\n  error1\n  error2"
