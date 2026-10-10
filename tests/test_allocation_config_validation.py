import unittest
from unittest.mock import patch, MagicMock

class TestAllocationConfigValidation(unittest.TestCase):
    def setUp(self):
        from usa_signal_bot.core.exceptions import AllocationMethodError
        self.dummy_exception = AllocationMethodError

        from usa_signal_bot.portfolio.allocation_methods import validate_allocation_config, AllocationConfig
        self.validate_allocation_config = validate_allocation_config

        # We need a mock enum for 'method' since it's a required argument
        method_mock = MagicMock()
        method_mock.value = "EQUAL_WEIGHT"

        self.valid_config = AllocationConfig(
            method=method_mock,
            max_total_allocation_pct=1.0,
            max_candidate_weight=0.10,
            min_candidate_weight=0.0,
            max_symbol_weight=0.15,
            max_strategy_weight=0.30,
            max_timeframe_weight=0.50,
            cash_buffer_pct=0.05,
            allow_fractional_quantity=True,
            normalize_weights=True
        )

    def tearDown(self):
        pass

    def test_valid_config(self):
        # Should not raise any exception
        self.validate_allocation_config(self.valid_config)

    def test_invalid_max_total_allocation_pct(self):
        self.valid_config.max_total_allocation_pct = 1.1
        with self.assertRaisesRegex(self.dummy_exception, "max_total_allocation_pct must be between 0 and 1."):
            self.validate_allocation_config(self.valid_config)

    def test_invalid_max_candidate_weight(self):
        self.valid_config.max_candidate_weight = -0.1
        with self.assertRaisesRegex(self.dummy_exception, "max_candidate_weight must be between 0 and 1."):
            self.validate_allocation_config(self.valid_config)

    def test_invalid_min_candidate_weight(self):
        self.valid_config.min_candidate_weight = 1.1
        with self.assertRaisesRegex(self.dummy_exception, "min_candidate_weight must be between 0 and 1."):
            self.validate_allocation_config(self.valid_config)

    def test_invalid_cash_buffer_pct(self):
        self.valid_config.cash_buffer_pct = -0.05
        with self.assertRaisesRegex(self.dummy_exception, "cash_buffer_pct must be between 0 and 1."):
            self.validate_allocation_config(self.valid_config)

    def test_min_greater_than_max(self):
        self.valid_config.min_candidate_weight = 0.5
        self.valid_config.max_candidate_weight = 0.4
        with self.assertRaisesRegex(self.dummy_exception, "min_candidate_weight cannot be greater than max_candidate_weight."):
            self.validate_allocation_config(self.valid_config)

if __name__ == '__main__':
    unittest.main()
