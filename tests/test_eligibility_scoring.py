
import unittest
from usa_signal_bot.research_governance.eligibility_scoring import calculate_promotion_eligibility_score
from usa_signal_bot.research_governance.governance_models import GovernanceEvidencePack, EvidencePackStatus, GovernanceChecklistItem, GovernanceChecklistStatus

class TestEligibilityScoring(unittest.TestCase):
    def test_eligibility(self):
        score = calculate_promotion_eligibility_score(
            GovernanceEvidencePack("1", "2", None, None, None, None, None, EvidencePackStatus.COMPLETE, [], [], [], {}, {}, {}, {}, [], []),
            [GovernanceChecklistItem("1", "1", GovernanceChecklistStatus.PASS, "1", [], [], [], [])]
        )
        self.assertEqual(score, 100.0)
