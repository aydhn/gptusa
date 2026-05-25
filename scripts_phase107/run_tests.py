import subprocess
print("Running pytest to check implementation...")
res = subprocess.run(["pytest", "tests/test_phase107_models.py", "tests/test_provider_abstraction_ingestion.py", "tests/test_cache_key_builder.py", "tests/test_cache_lookup_dry_run.py", "tests/test_fetch_dry_run_planner.py", "tests/test_fetch_dry_run_executor.py", "tests/test_provider_runtime_registry.py", "tests/test_provider_runtime_policy.py", "tests/test_provider_runtime_validator.py", "tests/test_provider_contract_test_runner.py", "tests/test_provider_fixture_factory.py", "tests/test_ohlcv_schema_validator.py", "tests/test_yfinance_adapter.py", "tests/test_stooq_adapter.py", "tests/test_local_csv_adapter.py", "tests/test_provider_runtime_report.py", "tests/test_provider_runtime_store.py", "tests/test_provider_runtime_validation.py", "tests/test_provider_runtime_reporting.py", "tests/test_cli_phase107.py"], capture_output=True, text=True)
print(res.stdout)
print(res.stderr)
