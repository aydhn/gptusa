
import unittest
from usa_signal_bot.research_governance.promotion_decision_log import create_promotion_decision_log_entry
from usa_signal_bot.research_governance.governance_models import PromotionDecision

class TestPromotionDecisionLog(unittest.TestCase):
    def test_promotion_decision_log(self):
        entry = create_promotion_decision_log_entry("test", "id1", PromotionDecision.REJECT, "reason")
        self.assertEqual(entry.entity_type, "test")
