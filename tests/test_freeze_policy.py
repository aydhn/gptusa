import unittest
from usa_signal_bot.provider_freeze.freeze_policy import build_default_provider_freeze_policy, validate_provider_freeze_policy

class TestFreezePolicy(unittest.TestCase):
    def test_default_policy_is_valid(self):
        policy = build_default_provider_freeze_policy()
        errors = validate_provider_freeze_policy(policy)
        self.assertEqual(len(errors), 0)
