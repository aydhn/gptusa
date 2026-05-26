import unittest
from usa_signal_bot.provider_freeze.rehearsal_runner import DataLayerRehearsalRunner

class TestRehearsalRunner(unittest.TestCase):
    def test_run(self):
        runner = DataLayerRehearsalRunner()
        report = runner.run()
        self.assertTrue(report.rehearsal_passed)
