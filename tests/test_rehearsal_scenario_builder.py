import unittest
from usa_signal_bot.provider_freeze.rehearsal_scenario_builder import build_default_rehearsal_scenarios, validate_rehearsal_scenario_safety

class TestScenarioBuilder(unittest.TestCase):
    def test_scenarios_valid(self):
        scenarios = build_default_rehearsal_scenarios()
        self.assertGreater(len(scenarios), 0)
        for s in scenarios:
            self.assertEqual(len(validate_rehearsal_scenario_safety(s)), 0)
