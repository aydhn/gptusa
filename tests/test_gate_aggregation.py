
import unittest
from usa_signal_bot.research_governance.gate_aggregation import count_gate_statuses

class TestGateAggregation(unittest.TestCase):
    def test_gate_aggregation(self):
        res = count_gate_statuses([{"status": "PASS"}, {"status": "FAIL"}])
        self.assertEqual(res["PASS"], 1)
        self.assertEqual(res["FAIL"], 1)
