from typing import List, Dict, Any
from usa_signal_bot.provider_quality.phase109_models import (
    ProviderDataQualityScore,
    DataQualityScoreComponent,
    ProviderSelectionScore
)

def validate_score_range(value: float | None, field_name: str = "score") -> List[str]:
    if value is None:
        return []
    if not (0.0 <= value <= 100.0):
        return [f"{field_name} must be between 0 and 100, got {value}"]
    return []

def validate_component_weights(components: List[DataQualityScoreComponent]) -> List[str]:
    weights = [c.weight for c in components]
    total = sum(weights)
    if total > 0 and abs(total - 1.0) > 0.01:
        return [f"Component weights sum to {total}, expected 1.0"]
    return []

def validate_quality_score_calibration(score: ProviderDataQualityScore) -> List[str]:
    errors = []
    errors.extend(validate_score_range(score.total_score, "total_score"))
    for c in score.components:
        errors.extend(validate_score_range(c.score, f"component {c.component.value} score"))
        if c.weighted_score > c.score:
            errors.append(f"Weighted score {c.weighted_score} exceeds base score {c.score} for {c.component.value}")
    errors.extend(validate_component_weights(score.components))
    return errors

def validate_selection_score_calibration(score: ProviderSelectionScore) -> List[str]:
    errors = []
    errors.extend(validate_score_range(score.final_selection_score, "final_selection_score"))
    errors.extend(validate_score_range(score.quality_score, "quality_score"))
    errors.extend(validate_score_range(score.trust_score, "trust_score"))
    errors.extend(validate_score_range(score.freshness_score, "freshness_score"))
    errors.extend(validate_score_range(score.safety_score, "safety_score"))
    errors.extend(validate_score_range(score.availability_score, "availability_score"))
    return errors

def score_calibration_guard_summary(errors: List[str]) -> Dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors),
        "errors": errors
    }

def score_calibration_guard_to_text(errors: List[str]) -> str:
    if not errors:
        return "Score Calibration Guard: PASSED"
    return "Score Calibration Guard: FAILED\n  " + "\n  ".join(errors)
