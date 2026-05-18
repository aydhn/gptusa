
import unittest
from usa_signal_bot.research_governance.drawdown_regime_regression import detect_drawdown_regression
from usa_signal_bot.research_governance.governance_models import GovernanceChecklistStatus

class TestDrawdownRegimeRegression(unittest.TestCase):
    def test_drawdown_regime(self):
        flags = detect_drawdown_regression(10.0, 15.0)
        self.assertEqual(flags.status, GovernanceChecklistStatus.WARNING)
