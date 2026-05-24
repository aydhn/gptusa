def normalize_cli_registry(registry: dict[str, str]) -> dict[str, str]:
    return registry.copy()

def phase102_cli_commands() -> dict[str, str]:
    return {
        "runtime-registry-info": "Shows info",
        "runtime-registry-transition-ingest": "Ingests transition review",
        "runtime-modes": "Shows runtime modes",
        "capability-policy": "Shows capability policies",
        "config-surface": "Shows config surface",
        "config-cleanup": "Performs config cleanup",
        "config-conflicts": "Checks for conflicts",
        "config-migration-hints": "Generates migration hints",
        "provider-contracts-info": "Shows provider contracts",
        "provider-manifest": "Generates provider manifest",
        "provider-safety": "Generates safety manifest",
        "provider-interface-validate": "Validates interfaces",
        "normalized-runtime-registry": "Builds normalized registry",
        "runtime-registry-review": "Generates full review",
        "runtime-registry-summary": "Shows store summary",
        "runtime-registry-validate": "Validates registry"
    }

def validate_normalized_cli_registry(registry: dict[str, str]) -> list[str]:
    return []

def cli_registry_normalizer_to_text(registry: dict[str, str]) -> str:
    return "CLI registry normalized."
