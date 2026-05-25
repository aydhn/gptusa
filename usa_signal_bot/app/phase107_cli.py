import argparse
import sys
from pathlib import Path

from usa_signal_bot.data_provider_runtime.phase107_models import *
from usa_signal_bot.data_provider_runtime.provider_abstraction_ingestion import ingest_latest_provider_abstraction_review_from_store
from usa_signal_bot.data_provider_runtime.provider_runtime_registry import build_provider_runtime_adapter_specs, provider_runtime_registry_to_text
from usa_signal_bot.data_provider_runtime.provider_runtime_policy import build_phase107_provider_runtime_policy, provider_runtime_policy_to_text
from usa_signal_bot.data_provider_runtime.cache_key_builder import build_provider_cache_key, provider_cache_key_to_text
from usa_signal_bot.data_provider_runtime.cache_lookup_dry_run import run_cache_lookup_dry_run, cache_lookup_dry_run_to_text
from usa_signal_bot.data_provider_runtime.fetch_dry_run_planner import build_default_market_data_dry_run_plans, fetch_dry_run_plan_to_text
from usa_signal_bot.data_provider_runtime.fetch_dry_run_executor import execute_fetch_dry_run_batch, fetch_dry_run_result_to_text
from usa_signal_bot.data_provider_runtime.provider_contract_test_runner import ProviderContractTestRunner
from usa_signal_bot.data_provider_runtime.provider_runtime_report import build_provider_runtime_context, build_provider_runtime_full_review, provider_runtime_full_review_to_text
from usa_signal_bot.data_provider_runtime.provider_runtime_store import *
from usa_signal_bot.data_provider_runtime.provider_runtime_validation import validate_provider_runtime_full_review_report, provider_runtime_validation_report_to_text
from usa_signal_bot.data_provider_runtime.provider_runtime_reporting import *

DATA_ROOT = Path("data")

def handle_provider_runtime_info(args):
    print("=== Phase 107 Provider Runtime Info ===")
    print("Phase 107 is NOT an activation phase.")
    print("It implements free market data provider adapters with cache-aware dry-runs.")
    print("Broker/Paper mutation/Scraping/Paid APIs are EXPLICITLY PROHIBITED.")

def handle_provider_runtime_ingest_abstraction(args):
    try:
        res = ingest_latest_provider_abstraction_review_from_store(DATA_ROOT)
        print(provider_abstraction_ingestion_result_to_text(res))
    except Exception as e:
        print(f"Error: {e}")

def handle_provider_runtime_policy(args):
    pol = build_phase107_provider_runtime_policy()
    print(provider_runtime_policy_to_text(pol))

def handle_provider_runtime_registry(args):
    specs = build_provider_runtime_adapter_specs()
    print(provider_runtime_registry_to_text(specs))

def handle_provider_cache_key(args):
    key = build_provider_cache_key("YFINANCE", "GET_DAILY_OHLCV", "AAPL")
    print(provider_cache_key_to_text(key))

def handle_provider_cache_lookup_dry_run(args):
    key = build_provider_cache_key("YFINANCE", "GET_DAILY_OHLCV", "AAPL")
    res = run_cache_lookup_dry_run(key, DATA_ROOT)
    print(cache_lookup_dry_run_to_text(res))

def handle_provider_fetch_dry_run_plan(args):
    plans = build_default_market_data_dry_run_plans(["AAPL"])
    for p in plans:
        print(fetch_dry_run_plan_to_text(p))

def handle_provider_fetch_dry_run(args):
    plans = build_default_market_data_dry_run_plans(["AAPL"])
    results = execute_fetch_dry_run_batch(plans, DATA_ROOT)
    for r in results:
        print(fetch_dry_run_result_to_text(r))

def handle_provider_contract_tests(args):
    specs = build_provider_runtime_adapter_specs()
    runner = ProviderContractTestRunner(specs)
    report = runner.run_all_contract_tests()
    print(provider_contract_test_report_to_text(report))

def handle_provider_fixture_sample(args):
    from usa_signal_bot.data_provider_runtime.provider_fixture_factory import sample_ohlcv_records
    records = sample_ohlcv_records("AAPL", 2)
    print(f"Sample Records: {records}")

def handle_ohlcv_schema_validate(args):
    from usa_signal_bot.data_provider_runtime.provider_fixture_factory import sample_ohlcv_dataframe
    from usa_signal_bot.data_provider_runtime.ohlcv_schema_validator import validate_ohlcv_dataframe, ohlcv_schema_validator_to_text
    df = sample_ohlcv_dataframe("AAPL", 5)
    errors = validate_ohlcv_dataframe(df)
    print(ohlcv_schema_validator_to_text(errors))

def handle_provider_runtime_context(args):
    ctx = build_provider_runtime_context()
    print(provider_runtime_context_to_text(ctx))

def handle_provider_runtime_review(args):
    ingest = ingest_latest_provider_abstraction_review_from_store(DATA_ROOT)
    specs = build_provider_runtime_adapter_specs()
    plans = build_default_market_data_dry_run_plans(["AAPL"])
    results = execute_fetch_dry_run_batch(plans, DATA_ROOT)
    runner = ProviderContractTestRunner(specs)
    report = runner.run_all_contract_tests()

    ctx = build_provider_runtime_context()
    ctx.ingestion = ingest
    ctx.adapter_specs = specs
    ctx.dry_run_plans = plans
    ctx.dry_run_results = results
    ctx.contract_test_report = report
    ctx.provider_runtime_ready = True

    review = build_provider_runtime_full_review()
    review.ingestion = ingest
    review.context = ctx
    review.adapter_specs = specs
    review.dry_run_plans = plans
    review.dry_run_results = results
    review.contract_test_report = report

    if args.write:
        write_provider_runtime_full_review_json(provider_runtime_reviews_dir(DATA_ROOT) / f"{review.review_id}.json", review)
        print("Review written to disk.")
    else:
        print(provider_runtime_full_review_to_text(review))

def handle_provider_runtime_summary(args):
    summary = provider_runtime_store_summary(DATA_ROOT)
    print(provider_runtime_store_summary_to_text(summary))

def handle_provider_runtime_validate(args):
    ingest = ingest_latest_provider_abstraction_review_from_store(DATA_ROOT)
    ctx = build_provider_runtime_context()
    ctx.ingestion = ingest
    review = build_provider_runtime_full_review()
    review.context = ctx
    report = validate_provider_runtime_full_review_report(review)
    print(provider_runtime_validation_report_to_text(report))
