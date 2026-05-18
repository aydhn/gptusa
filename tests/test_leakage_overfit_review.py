
import unittest
from usa_signal_bot.research_governance.leakage_overfit_review import detect_possible_leakage
from usa_signal_bot.research_governance.governance_models import GovernanceChecklistStatus

class TestLeakageOverfitReview(unittest.TestCase):
    def test_leakage_overfit(self):
        flags = detect_possible_leakage({"gates": [{"name": "NO_LEAKAGE", "status": "FAIL"}]})
        self.assertEqual(flags.status, GovernanceChecklistStatus.FAIL)
