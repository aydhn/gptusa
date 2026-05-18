
import unittest
from usa_signal_bot.research_governance.governance_validation import validate_no_live_execution_language_in_governance

class TestGovernanceValidation(unittest.TestCase):
    def test_validation(self):
        res = validate_no_live_execution_language_in_governance("This is a test sent to broker")
        self.assertFalse(res.valid)
