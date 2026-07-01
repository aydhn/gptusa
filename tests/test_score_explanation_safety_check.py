import unittest
from usa_signal_bot.provider_quality.score_explanation import score_explanation_safety_check

class TestScoreExplanationSafetyCheck(unittest.TestCase):
    def test_happy_path_safe_text(self):
        text = "The provider data is deemed USABLE FOR RESEARCH. Freshness scored 90."
        errors = score_explanation_safety_check(text)
        self.assertEqual(errors, [])

    def test_single_unsafe_term(self):
        text = "This provider gives a great trade signal."
        errors = score_explanation_safety_check(text)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0], "Unsafe term detected in explanation: 'trade signal'")

    def test_multiple_unsafe_terms(self):
        text = "Buy signal detected, order execution guaranteed."
        errors = score_explanation_safety_check(text)
        self.assertEqual(len(errors), 4)
        self.assertIn("Unsafe term detected in explanation: 'buy signal'", errors)
        self.assertIn("Unsafe term detected in explanation: 'order'", errors)
        self.assertIn("Unsafe term detected in explanation: 'execution'", errors)
        self.assertIn("Unsafe term detected in explanation: 'guarantee'", errors)

    def test_case_insensitivity(self):
        text = "This is a pOrTfOlIo recommendation with a GuaRanTee."
        errors = score_explanation_safety_check(text)
        self.assertEqual(len(errors), 2)
        self.assertIn("Unsafe term detected in explanation: 'portfolio'", errors)
        self.assertIn("Unsafe term detected in explanation: 'guarantee'", errors)

    def test_substring_handling(self):
        text = "There are no borders."
        errors = score_explanation_safety_check(text)
        self.assertEqual(len(errors), 1)
        self.assertIn("Unsafe term detected in explanation: 'order'", errors)

if __name__ == "__main__":
    unittest.main()
