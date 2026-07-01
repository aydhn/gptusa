import unittest
from unittest.mock import MagicMock, patch
from usa_signal_bot.provider_quality.score_explanation import explain_provider_selection

class TestExplainProviderSelection(unittest.TestCase):
    @patch('usa_signal_bot.provider_quality.score_explanation.score_explanation_safety_check')
    def test_explain_provider_selection_success(self, mock_safety_check):
        mock_safety_check.return_value = []

        score = MagicMock()
        score.provider_name = "TestProvider"
        score.final_selection_score = 85.5
        score.status.value = "SELECTED"
        score.decision.value = "PRIMARY"
        score.blocked = False

        result = explain_provider_selection(score)

        self.assertIn("Provider Selection Score for TestProvider is 85.5 (SELECTED).", result)
        self.assertIn("Decision logic assigned: PRIMARY.", result)
        self.assertNotIn("Selection is explicitly blocked.", result)

    @patch('usa_signal_bot.provider_quality.score_explanation.score_explanation_safety_check')
    def test_explain_provider_selection_blocked(self, mock_safety_check):
        mock_safety_check.return_value = []

        score = MagicMock()
        score.provider_name = "BadProvider"
        score.final_selection_score = 20.0
        score.status.value = "REJECTED"
        score.decision.value = "NONE"
        score.blocked = True

        result = explain_provider_selection(score)

        self.assertIn("Provider Selection Score for BadProvider is 20.0 (REJECTED).", result)
        self.assertIn("Decision logic assigned: NONE.", result)
        self.assertIn("Selection is explicitly blocked.", result)

    @patch('usa_signal_bot.provider_quality.score_explanation.score_explanation_safety_check')
    def test_explain_provider_selection_unsafe_language(self, mock_safety_check):
        mock_safety_check.return_value = ["Unsafe term detected"]

        score = MagicMock()
        score.provider_name = "ShadyProvider"
        score.final_selection_score = 90.0
        score.status.value = "SELECTED"
        score.decision.value = "GUARANTEED_SIGNALS" # Doesn't matter what this is since we mock the safety check
        score.blocked = False

        result = explain_provider_selection(score)

        self.assertEqual(result, "Explanation blocked due to unsafe language.")
