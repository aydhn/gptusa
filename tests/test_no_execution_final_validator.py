import unittest
from usa_signal_bot.provider_freeze.no_execution_final_validator import validate_no_execution_final
from usa_signal_bot.provider_freeze.phase114_models import ProviderFreezeContext

class TestNoExecutionFinalValidator(unittest.TestCase):
    def test_validator(self):
        ctx = ProviderFreezeContext(context_id="test", created_at_utc="test")
        errors = validate_no_execution_final(context=ctx)
        self.assertEqual(len(errors), 0)
