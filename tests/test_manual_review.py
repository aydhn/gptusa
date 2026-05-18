
import unittest
from usa_signal_bot.research_governance.manual_review import manual_review_required_for_flags
from usa_signal_bot.research_governance.governance_models import GovernanceRiskFlag

class TestManualReview(unittest.TestCase):
    def test_manual_review(self):
        req = manual_review_required_for_flags([GovernanceRiskFlag.POSSIBLE_LEAKAGE])
        self.assertTrue(req)
