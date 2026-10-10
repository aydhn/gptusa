import pytest
import sys
from typing import Dict
from unittest.mock import patch, MagicMock

# The module has a systemic ImportError (DataQualityComponent is missing in enums.py)
# We will use MagicMock to simulate the enum in the test since out-of-scope files shouldn't be touched

from usa_signal_bot.provider_quality.scoring_policy import (
    build_default_provider_quality_scoring_policy,
    validate_scoring_policy,
    normalize_scoring_weights,
    scoring_policy_component_weight,
    scoring_policy_to_text,
)

def test_build_default_provider_quality_scoring_policy():
    policy = build_default_provider_quality_scoring_policy()
    assert isinstance(policy, dict)
    assert "COMPLETENESS" in policy
    assert "FRESHNESS" in policy
    assert "SCHEMA_VALIDITY" in policy
    assert "CONTINUITY" in policy
    assert "SOURCE_AGREEMENT" in policy
    assert "OUTLIER_PROFILE" in policy
    assert "CACHE_RELIABILITY" in policy
    assert "SAFETY_COMPLIANCE" in policy

    # Check sum is 1.0 (or very close)
    total = sum(policy.values())
    assert abs(total - 1.0) < 1e-6

def test_validate_scoring_policy():
    # Valid policy
    valid_policy = {"A": 0.5, "B": 0.5}
    assert validate_scoring_policy(valid_policy) == []

    # Invalid sum
    invalid_sum = {"A": 0.5, "B": 0.6}
    errors = validate_scoring_policy(invalid_sum)
    assert len(errors) == 1
    assert "sum to 1.1" in errors[0]

    # Invalid weights (< 0)
    invalid_weight_low = {"A": 1.1, "B": -0.1}
    errors = validate_scoring_policy(invalid_weight_low)
    assert len(errors) == 2 # weight A is > 1, weight B is < 0
    assert "must be between 0 and 1" in errors[0]

    # Invalid weights (> 1)
    invalid_weight_high = {"A": 1.2, "B": -0.2}
    errors = validate_scoring_policy(invalid_weight_high)
    assert len(errors) == 2 # weight A > 1, weight B < 0
    assert any("must be between 0 and 1" in e for e in errors)

def test_normalize_scoring_weights():
    # Already normalized
    policy = {"A": 0.5, "B": 0.5}
    assert normalize_scoring_weights(policy) == policy

    # Needs normalization
    policy = {"A": 1.0, "B": 3.0} # sum = 4.0
    normalized = normalize_scoring_weights(policy)
    assert normalized["A"] == 0.25
    assert normalized["B"] == 0.75

    # Zero sum
    policy = {"A": 0.0, "B": 0.0}
    assert normalize_scoring_weights(policy) == policy


def test_scoring_policy_component_weight():
    # With provided policy
    policy = {"TEST_COMPONENT": 0.42}
    component = MagicMock(value="TEST_COMPONENT")
    assert scoring_policy_component_weight(component, policy) == 0.42

    # Component not in policy
    component_not_in = MagicMock(value="MISSING")
    assert scoring_policy_component_weight(component_not_in, policy) == 0.0

    # Without provided policy (uses default)
    # COMPLETENESS is 0.20 in default
    component_completeness = MagicMock(value="COMPLETENESS")
    assert scoring_policy_component_weight(component_completeness) == 0.20

def test_scoring_policy_to_text():
    policy = {"A": 0.5, "B": 0.1234}
    text = scoring_policy_to_text(policy)
    assert "Scoring Policy Weights:" in text
    assert "  A: 0.50" in text
    assert "  B: 0.12" in text
