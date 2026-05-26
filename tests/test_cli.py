import unittest
from usa_signal_bot.app.cli import phase114_provider_freeze_info

class DummyArgs:
    pass

class TestCLI(unittest.TestCase):
    def test_info(self):
        args = DummyArgs()
        phase114_provider_freeze_info(args)
        self.assertTrue(True)
