
import unittest
from usa_signal_bot.research_governance.cost_turnover_regression import detect_cost_drag_regression
from usa_signal_bot.research_governance.governance_models import GovernanceChecklistStatus

class TestCostTurnoverRegression(unittest.TestCase):
    def test_cost_turnover(self):
        flags = detect_cost_drag_regression(1.0, 2.0)
        self.assertEqual(flags.status, GovernanceChecklistStatus.WARNING)
