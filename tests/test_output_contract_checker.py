import unittest
from usa_signal_bot.provider_freeze.output_contract_checker import build_data_layer_output_contract, validate_data_layer_output_contract

class TestOutputContractChecker(unittest.TestCase):
    def test_contract(self):
        contract = build_data_layer_output_contract()
        errors = validate_data_layer_output_contract(contract)
        self.assertEqual(len(errors), 0)
