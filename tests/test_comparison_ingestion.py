
import unittest
from usa_signal_bot.research_governance.comparison_ingestion import extract_comparison_ids

class TestComparisonIngestion(unittest.TestCase):
    def test_extract(self):
        ids = extract_comparison_ids({"baseline_run_id": "b1"})
        self.assertEqual(ids["baseline_run_id"], "b1")
