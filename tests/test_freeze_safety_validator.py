import unittest
from usa_signal_bot.provider_freeze.freeze_safety_validator import validate_provider_freeze_context_safety
from usa_signal_bot.provider_freeze.phase114_models import ProviderFreezeContext

class TestFreezeSafetyValidator(unittest.TestCase):
    def test_safety(self):
        ctx = ProviderFreezeContext(context_id="test", created_at_utc="test")
        errors = validate_provider_freeze_context_safety(ctx)
        self.assertEqual(len(errors), 0)
