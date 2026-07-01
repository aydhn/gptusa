import unittest
from unittest.mock import patch, MagicMock

from usa_signal_bot.provider_quality.score_explanation import explain_source_trust

class DummyTrustLevel:
    def __init__(self, value):
        self.value = value

class TestExplainSourceTrust(unittest.TestCase):
    def setUp(self):
        self.mock_profile = MagicMock()
        self.mock_profile.provider_name = "TestProvider"
        self.mock_profile.trust_score = 85.5

    def test_explain_source_trust_high_trust(self):
        self.mock_profile.trust_level = DummyTrustLevel("HIGH_TRUST")

        result = explain_source_trust(self.mock_profile)

        self.assertEqual(result, "Source Trust Profile for TestProvider indicates HIGH_TRUST with a score of 85.5.")

    def test_explain_source_trust_untrusted(self):
        self.mock_profile.trust_level = DummyTrustLevel("UNTRUSTED")
        self.mock_profile.trust_score = 25.0

        result = explain_source_trust(self.mock_profile)

        expected = "Source Trust Profile for TestProvider indicates UNTRUSTED with a score of 25.0. Source is heavily untrusted and should generally be avoided."
        self.assertEqual(result, expected)

    def test_explain_source_trust_blocked(self):
        self.mock_profile.trust_level = DummyTrustLevel("BLOCKED")
        self.mock_profile.trust_score = 10.0

        result = explain_source_trust(self.mock_profile)

        expected = "Source Trust Profile for TestProvider indicates BLOCKED with a score of 10.0. Source is blocked due to severe reliability or safety failures."
        self.assertEqual(result, expected)

    @patch("usa_signal_bot.provider_quality.score_explanation.score_explanation_safety_check")
    def test_explain_source_trust_unsafe_language(self, mock_safety_check):
        self.mock_profile.trust_level = DummyTrustLevel("HIGH_TRUST")

        # Mock safety check to return errors
        mock_safety_check.return_value = ["Unsafe term detected in explanation: 'trade signal'"]

        result = explain_source_trust(self.mock_profile)

        self.assertEqual(result, "Explanation blocked due to unsafe language.")

if __name__ == '__main__':
    unittest.main()
