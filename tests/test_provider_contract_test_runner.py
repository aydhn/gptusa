from usa_signal_bot.data_provider_runtime.provider_runtime_registry import build_provider_runtime_adapter_specs
from usa_signal_bot.data_provider_runtime.provider_contract_test_runner import ProviderContractTestRunner

def test_provider_contract_test_runner():
    specs = build_provider_runtime_adapter_specs()
    runner = ProviderContractTestRunner(specs)
    report = runner.run_all_contract_tests()
    assert report.contract_tests_passed is True
    assert report.failed_tests == 0
