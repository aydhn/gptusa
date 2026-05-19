
import unittest
from usa_signal_bot.research_governance.risk_regression import detect_metric_regression
from usa_signal_bot.research_governance.governance_models import GovernanceChecklistStatus

class TestRiskRegression(unittest.TestCase):
    def test_risk_regression(self):
        flags = detect_metric_regression("max_dd", 10.0, 15.0, False)
        self.assertEqual(flags.status, GovernanceChecklistStatus.WARNING)
