import unittest
from usa_signal_bot.portfolio.concentration_guards import validate_concentration_guard_config, ConcentrationGuardConfig
from usa_signal_bot.core.exceptions import ConcentrationGuardError

class TestConcentrationGuardConfigValidation(unittest.TestCase):

    def test_valid_config(self):
        config = ConcentrationGuardConfig(
            max_symbol_weight=0.15,
            max_strategy_weight=0.30,
            max_timeframe_weight=0.50,
            max_single_candidate_weight=0.10,
            reject_breaches=False,
            cap_breaches=True
        )
        # Should not raise
        validate_concentration_guard_config(config)

    def test_invalid_config_negative(self):
        config = ConcentrationGuardConfig(
            max_symbol_weight=-0.05,
            max_strategy_weight=0.30,
            max_timeframe_weight=0.50,
            max_single_candidate_weight=0.10
        )
        with self.assertRaisesRegex(ConcentrationGuardError, "All concentration guard limits must be between 0 and 1."):
            validate_concentration_guard_config(config)

    def test_invalid_config_too_high(self):
        config = ConcentrationGuardConfig(
            max_symbol_weight=0.15,
            max_strategy_weight=0.30,
            max_timeframe_weight=1.50,
            max_single_candidate_weight=0.10
        )
        with self.assertRaisesRegex(ConcentrationGuardError, "All concentration guard limits must be between 0 and 1."):
            validate_concentration_guard_config(config)

if __name__ == '__main__':
    unittest.main()
