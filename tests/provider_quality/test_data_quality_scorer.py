import unittest
from usa_signal_bot.provider_quality.data_quality_scorer import data_quality_grade_from_score

class TestDataQualityScorer(unittest.TestCase):
    def test_data_quality_grade_from_score(self):
        self.assertEqual(data_quality_grade_from_score(100).value, "EXCELLENT")
        self.assertEqual(data_quality_grade_from_score(90).value, "EXCELLENT")
        self.assertEqual(data_quality_grade_from_score(89.9).value, "GOOD")
        self.assertEqual(data_quality_grade_from_score(80).value, "GOOD")
        self.assertEqual(data_quality_grade_from_score(79.9).value, "ACCEPTABLE")
        self.assertEqual(data_quality_grade_from_score(65).value, "ACCEPTABLE")
        self.assertEqual(data_quality_grade_from_score(64.9).value, "WEAK")
        self.assertEqual(data_quality_grade_from_score(40).value, "WEAK")
        self.assertEqual(data_quality_grade_from_score(39.9).value, "POOR")
        self.assertEqual(data_quality_grade_from_score(0).value, "POOR")
        self.assertEqual(data_quality_grade_from_score(-10).value, "POOR")
        self.assertEqual(data_quality_grade_from_score(100, blocked=True).value, "BLOCKED")
        self.assertEqual(data_quality_grade_from_score(0, blocked=True).value, "BLOCKED")

if __name__ == "__main__":
    unittest.main()
