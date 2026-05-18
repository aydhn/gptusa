
import unittest
from usa_signal_bot.research_governance.governance_models import GovernanceChecklistItem, GovernanceChecklistStatus

class TestGovernanceModels(unittest.TestCase):
    def test_governance_models(self):
        item = GovernanceChecklistItem("c1", "name", GovernanceChecklistStatus.PASS, "desc", [], [], [], [])
        self.assertEqual(item.name, "name")
