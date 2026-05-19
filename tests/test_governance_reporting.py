
import unittest
from usa_signal_bot.research_governance.governance_reporting import governance_limitations_text

class TestGovernanceReporting(unittest.TestCase):
    def test_reporting(self):
        text = governance_limitations_text()
        self.assertTrue("PASS is not live approval" in text)
