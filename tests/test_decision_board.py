
import unittest
from usa_signal_bot.research_governance.decision_board import GovernanceDecisionBoard
from usa_signal_bot.research_governance.governance_models import PromotionDecision

class TestDecisionBoard(unittest.TestCase):
    def test_decision_board(self):
        board = GovernanceDecisionBoard()
        review = board.review_comparison_report({"gates": [{"name": "NO_LEAKAGE", "status": "FAIL"}]})
        self.assertEqual(review.proposed_decision, PromotionDecision.BLOCK)
