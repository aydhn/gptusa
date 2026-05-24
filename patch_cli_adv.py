import re

with open("usa_signal_bot/app/cli.py", "r") as f:
    content = f.read()

new_commands = """
@cli.command("runtime-registry-info")
def runtime_registry_info():
    print("Phase 102 Advanced Runtime Registry Normalization.")
    print("This is NOT an activation phase. No real execution allowed.")

@cli.command("runtime-registry-transition-ingest")
@click.option("--write", is_flag=True)
def runtime_registry_transition_ingest(write):
    from usa_signal_bot.advanced_runtime.transition_review_ingestion import ingest_advanced_transition_review_payload
    res = ingest_advanced_transition_review_payload({"review_id": "test"})
    print(f"Ingested: {res.ingestion_id}")

@cli.command("runtime-modes")
def runtime_modes():
    from usa_signal_bot.advanced_runtime.runtime_mode_registry import build_phase102_runtime_modes
    print(f"Modes built: {len(build_phase102_runtime_modes())}")

@cli.command("capability-policy")
def capability_policy():
    from usa_signal_bot.advanced_runtime.capability_policy import build_phase102_capability_policies
    print(f"Policies built: {len(build_phase102_capability_policies())}")

@cli.command("config-surface")
def config_surface():
    from usa_signal_bot.advanced_runtime.config_surface import build_config_surface_records
    print(f"Config surface built: {len(build_config_surface_records({}))}")

@cli.command("config-cleanup")
def config_cleanup():
    from usa_signal_bot.advanced_runtime.config_cleanup import normalize_config_surface
    res = normalize_config_surface({})
    print(f"Config cleanup done.")

@cli.command("config-conflicts")
def config_conflicts():
    from usa_signal_bot.advanced_runtime.config_conflict_detector import detect_config_conflicts
    print(f"Conflicts: {detect_config_conflicts({})}")

@cli.command("config-migration-hints")
def config_migration_hints():
    from usa_signal_bot.advanced_runtime.config_migration_hints import generate_config_migration_hints
    print(f"Hints: {generate_config_migration_hints({})}")

@cli.command("provider-contracts-info")
def provider_contracts_info():
    from usa_signal_bot.advanced_runtime.provider_contracts import build_provider_data_request
    from usa_signal_bot.core.enums import ProviderInterfaceKind, ProviderCapability
    req = build_provider_data_request("test", ProviderInterfaceKind.MARKET_DATA, ProviderCapability.GET_DAILY_BARS)
    print(f"Request: {req.request_id}")

@cli.command("provider-manifest")
@click.option("--write", is_flag=True)
def provider_manifest(write):
    from usa_signal_bot.advanced_runtime.provider_capability_manifest import default_market_data_provider_manifest
    print(f"Manifest: {default_market_data_provider_manifest('yfinance').manifest_id}")

@cli.command("provider-safety")
@click.option("--write", is_flag=True)
def provider_safety(write):
    from usa_signal_bot.advanced_runtime.provider_safety_manifest import build_provider_safety_manifest
    print(f"Safety: {build_provider_safety_manifest('yfinance').manifest_id}")

@cli.command("provider-interface-validate")
def provider_interface_validate():
    from usa_signal_bot.advanced_runtime.provider_interface_validator import validate_provider_interface_contract
    print(f"Validation: {validate_provider_interface_contract(None)}")

@cli.command("normalized-runtime-registry")
@click.option("--write", is_flag=True)
def normalized_runtime_registry(write):
    from usa_signal_bot.advanced_runtime.normalized_runtime_registry import build_default_normalized_runtime_registry
    print(f"Registry: {build_default_normalized_runtime_registry().registry_id}")

@cli.command("runtime-registry-review")
@click.option("--write", is_flag=True)
def runtime_registry_review(write):
    from usa_signal_bot.advanced_runtime.runtime_registry_report import build_runtime_registry_full_review
    print(f"Review: {build_runtime_registry_full_review().review_id}")

@cli.command("runtime-registry-summary")
def runtime_registry_summary():
    from pathlib import Path
    from usa_signal_bot.advanced_runtime.runtime_registry_store import runtime_registry_store_summary
    print(f"Summary: {runtime_registry_store_summary(Path('data'))}")

@cli.command("runtime-registry-validate")
def runtime_registry_validate():
    from usa_signal_bot.advanced_runtime.runtime_registry_validation import validate_no_execution_language_in_runtime_registry_text
    print(f"Valid: {validate_no_execution_language_in_runtime_registry_text('test text').valid}")
"""

if "@cli.command(\"runtime-registry-info\")" not in content:
    content = content + "\n" + new_commands + "\n"
    with open("usa_signal_bot/app/cli.py", "w") as f:
        f.write(content)
