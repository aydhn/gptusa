import unittest
from usa_signal_bot.provider_freeze.rehearsal_runner import DataLayerRehearsalRunner
from usa_signal_bot.provider_freeze.rehearsal_validator import validate_data_layer_rehearsal_report

class TestRehearsalValidator(unittest.TestCase):
    def test_validate(self):
        runner = DataLayerRehearsalRunner()
        report = runner.run()
        errors = validate_data_layer_rehearsal_report(report)
        self.assertEqual(len(errors), 0)
