import unittest
from unittest.mock import MagicMock

from usa_signal_bot.core.enums import DataQualityComponent
from usa_signal_bot.provider_quality.scoring_policy import (
    build_default_provider_quality_scoring_policy,
    validate_scoring_policy,
    normalize_scoring_weights,
    scoring_policy_component_weight,
    scoring_policy_to_text,
)

class TestScoringPolicy(unittest.TestCase):
    def test_build_default_provider_quality_scoring_policy(self):
        policy = build_default_provider_quality_scoring_policy()
        self.assertIsInstance(policy, dict)
        self.assertIn("COMPLETENESS", policy)
        self.assertIn("FRESHNESS", policy)
        self.assertIn("SCHEMA_VALIDITY", policy)
        self.assertIn("CONTINUITY", policy)
        self.assertIn("SOURCE_AGREEMENT", policy)
        self.assertIn("OUTLIER_PROFILE", policy)
        self.assertIn("CACHE_RELIABILITY", policy)
        self.assertIn("SAFETY_COMPLIANCE", policy)

        # Check sum is 1.0 (or very close)
        total = sum(policy.values())
        self.assertTrue(abs(total - 1.0) < 1e-6)

    def test_validate_scoring_policy(self):
        # Valid policy
        valid_policy = {"A": 0.5, "B": 0.5}
        self.assertEqual(validate_scoring_policy(valid_policy), [])

        # Invalid sum
        invalid_sum = {"A": 0.5, "B": 0.6}
        errors = validate_scoring_policy(invalid_sum)
        self.assertEqual(len(errors), 1)
        self.assertIn("sum to 1.1", errors[0])

        # Invalid weights (< 0)
        invalid_weight_low = {"A": 1.1, "B": -0.1}
        errors = validate_scoring_policy(invalid_weight_low)
        self.assertEqual(len(errors), 2) # weight A is > 1, weight B is < 0
        self.assertIn("must be between 0 and 1", errors[0])

        # Invalid weights (> 1)
        invalid_weight_high = {"A": 1.2, "B": -0.2}
        errors = validate_scoring_policy(invalid_weight_high)
        self.assertEqual(len(errors), 2) # weight A > 1, weight B < 0
        self.assertTrue(any("must be between 0 and 1" in e for e in errors))

    def test_normalize_scoring_weights(self):
        # Already normalized
        policy = {"A": 0.5, "B": 0.5}
        self.assertEqual(normalize_scoring_weights(policy), policy)

        # Needs normalization
        policy = {"A": 1.0, "B": 3.0} # sum = 4.0
        normalized = normalize_scoring_weights(policy)
        self.assertEqual(normalized["A"], 0.25)
        self.assertEqual(normalized["B"], 0.75)

        # Zero sum
        policy = {"A": 0.0, "B": 0.0}
        self.assertEqual(normalize_scoring_weights(policy), policy)

    def test_scoring_policy_component_weight(self):
        # With provided policy
        policy = {"TEST_COMPONENT": 0.42}
        component = MagicMock()
        component.value = "TEST_COMPONENT"
        self.assertEqual(scoring_policy_component_weight(component, policy), 0.42)

        # Component not in policy
        component_not_in = MagicMock()
        component_not_in.value = "MISSING"
        self.assertEqual(scoring_policy_component_weight(component_not_in, policy), 0.0)

        # Without provided policy (uses default)
        # COMPLETENESS is 0.20 in default
        component_completeness = MagicMock()
        component_completeness.value = "COMPLETENESS"
        self.assertEqual(scoring_policy_component_weight(component_completeness), 0.20)

    def test_scoring_policy_to_text(self):
        policy = {"A": 0.5, "B": 0.1234}
        text = scoring_policy_to_text(policy)
        self.assertIn("Scoring Policy Weights:", text)
        self.assertIn("  A: 0.50", text)
        self.assertIn("  B: 0.12", text)

if __name__ == "__main__":
    unittest.main()
