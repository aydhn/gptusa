import re

with open("usa_signal_bot/app/cli.py", "r") as f:
    content = f.read()

ADDITION = """
def setup_phase107_parsers(subparsers):
    import usa_signal_bot.app.phase107_cli as p107
    subparsers.add_parser("provider-runtime-info", help="Info for phase 107").set_defaults(func=p107.handle_provider_runtime_info)
    subparsers.add_parser("provider-runtime-ingest-abstraction", help="Ingest abstraction review").set_defaults(func=p107.handle_provider_runtime_ingest_abstraction)
    subparsers.add_parser("provider-runtime-policy", help="Show policy").set_defaults(func=p107.handle_provider_runtime_policy)
    subparsers.add_parser("provider-runtime-registry", help="Show registry specs").set_defaults(func=p107.handle_provider_runtime_registry)
    subparsers.add_parser("provider-cache-key", help="Build cache key").set_defaults(func=p107.handle_provider_cache_key)
    subparsers.add_parser("provider-cache-lookup-dry-run", help="Cache lookup dry-run").set_defaults(func=p107.handle_provider_cache_lookup_dry_run)
    subparsers.add_parser("provider-fetch-dry-run-plan", help="Fetch dry-run plan").set_defaults(func=p107.handle_provider_fetch_dry_run_plan)
    subparsers.add_parser("provider-fetch-dry-run", help="Fetch dry-run execute").set_defaults(func=p107.handle_provider_fetch_dry_run)
    subparsers.add_parser("provider-contract-tests", help="Run contract tests").set_defaults(func=p107.handle_provider_contract_tests)
    subparsers.add_parser("provider-fixture-sample", help="Sample OHLCV").set_defaults(func=p107.handle_provider_fixture_sample)
    subparsers.add_parser("ohlcv-schema-validate", help="Validate OHLCV").set_defaults(func=p107.handle_ohlcv_schema_validate)
    subparsers.add_parser("provider-runtime-context", help="Show context").set_defaults(func=p107.handle_provider_runtime_context)

    review_parser = subparsers.add_parser("provider-runtime-review", help="Full review")
    review_parser.add_argument("--write", action="store_true")
    review_parser.set_defaults(func=p107.handle_provider_runtime_review)

    subparsers.add_parser("provider-runtime-summary", help="Store summary").set_defaults(func=p107.handle_provider_runtime_summary)
    subparsers.add_parser("provider-runtime-validate", help="Validate review").set_defaults(func=p107.handle_provider_runtime_validate)
"""

if "setup_phase107_parsers" not in content:
    content = ADDITION + "\n" + content
    content = content.replace(
        "def build_parser():",
        "def build_parser():"
    )
    content = content.replace(
        "    setup_no_write_admission_parsers(subparsers)",
        "    setup_no_write_admission_parsers(subparsers)\n    setup_phase107_parsers(subparsers)"
    )

    with open("usa_signal_bot/app/cli.py", "w") as f:
        f.write(content)
