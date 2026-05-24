from typing import Dict, List

def build_phase101_cli_registry() -> Dict[str, str]:
    return {
        "advanced-transition-info": "Show advanced transition info",
        "advanced-transition-ingest-handoff": "Ingest handoff freeze",
        "advanced-transition-roadmap": "Show roadmap",
        "advanced-transition-capabilities": "Show capabilities",
        "advanced-transition-runtime-boundary": "Show boundary",
        "advanced-transition-module-inventory": "Show inventory",
        "advanced-transition-config-check": "Check config",
        "advanced-transition-storage-registry": "Show storage",
        "advanced-transition-validation-registry": "Show validation",
        "advanced-transition-health-registry": "Show health",
        "advanced-transition-review": "Run full review",
        "advanced-transition-summary": "Show summary",
        "advanced-transition-validate": "Validate setup"
    }

def validate_cli_registry(registry: Dict[str, str]) -> List[str]:
    errors = []
    if "advanced-transition-info" not in registry:
        errors.append("Missing advanced-transition-info")
    return errors

def cli_registry_to_text(registry: Dict[str, str]) -> str:
    return "\n".join([f"{k}: {v}" for k, v in registry.items()])
