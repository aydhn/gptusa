import os

files_to_check = [
    "usa_signal_bot/data_provider_runtime/__init__.py",
    "usa_signal_bot/data_provider_runtime/phase107_models.py",
    "usa_signal_bot/data_provider_runtime/provider_abstraction_ingestion.py",
    "usa_signal_bot/data_provider_runtime/cache_key_builder.py",
    "usa_signal_bot/data_provider_runtime/cache_lookup_dry_run.py",
    "usa_signal_bot/data_provider_runtime/fetch_dry_run_planner.py",
    "usa_signal_bot/data_provider_runtime/fetch_dry_run_executor.py",
    "usa_signal_bot/data_provider_runtime/provider_runtime_registry.py",
    "usa_signal_bot/data_provider_runtime/provider_runtime_policy.py",
    "usa_signal_bot/data_provider_runtime/provider_runtime_validator.py",
    "usa_signal_bot/data_provider_runtime/provider_contract_test_runner.py",
    "usa_signal_bot/data_provider_runtime/provider_fixture_factory.py",
    "usa_signal_bot/data_provider_runtime/ohlcv_schema_validator.py",
    "usa_signal_bot/data_provider_runtime/provider_runtime_report.py",
    "usa_signal_bot/data_provider_runtime/provider_runtime_store.py",
    "usa_signal_bot/data_provider_runtime/provider_runtime_validation.py",
    "usa_signal_bot/data_provider_runtime/provider_runtime_reporting.py",
    "usa_signal_bot/data_providers/interfaces/base.py",
    "usa_signal_bot/data_providers/interfaces/market_data.py",
    "usa_signal_bot/data_providers/adapters/yfinance_adapter.py",
    "usa_signal_bot/data_providers/adapters/stooq_adapter.py",
    "usa_signal_bot/data_providers/adapters/local_csv_adapter.py",
    "tests/test_phase107_models.py",
    "docs/PHASE_107_FREE_MARKET_DATA_PROVIDER_IMPLEMENTATION.md"
]

missing = []
for f in files_to_check:
    if not os.path.exists(f):
        missing.append(f)

if missing:
    print("Missing files:")
    for m in missing:
        print(f" - {m}")
else:
    print("All files present.")
