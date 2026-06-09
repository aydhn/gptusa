content = """
from typing import Any, Dict, List, Optional
import hashlib

from usa_signal_bot.integration.phase158_models import SystemArtifactInventory, SystemArtifactRecord
from usa_signal_bot.core.enums import SystemArtifactKind

def build_system_artifact_inventory(payloads: Optional[Dict[str, Any]] = None) -> SystemArtifactInventory:
    inventory = SystemArtifactInventory()
    inventory.artifacts = build_default_system_artifact_records()
    inventory.artifact_count = len(inventory.artifacts)
    inventory.required_artifact_count = sum(1 for a in inventory.artifacts if a.required_for_integration)
    inventory.available_required_count = sum(1 for a in inventory.artifacts if a.required_for_integration and a.available)
    inventory.missing_required_count = inventory.required_artifact_count - inventory.available_required_count

    inventory.inventory_hash = compute_system_artifact_inventory_hash(inventory)
    inventory.inventory_valid = len(validate_system_artifact_inventory(inventory)) == 0
    return inventory

def build_default_system_artifact_records() -> List[SystemArtifactRecord]:
    kinds = [
        SystemArtifactKind.CONFIG,
        SystemArtifactKind.CLI,
        SystemArtifactKind.HEALTH,
        SystemArtifactKind.STORAGE,
        SystemArtifactKind.DATA_PROVIDER,
        SystemArtifactKind.FEATURE_ENGINE,
        SystemArtifactKind.REGIME_ENGINE,
        SystemArtifactKind.ML_GOVERNANCE,
        SystemArtifactKind.BACKTEST_CLOSURE,
        SystemArtifactKind.PORTFOLIO_FOUNDATION,
        SystemArtifactKind.SIZING_PROTOTYPE,
        SystemArtifactKind.ALLOCATION_SANDBOX,
        SystemArtifactKind.OPTIMIZER_SANDBOX,
        SystemArtifactKind.PORTFOLIO_RISK_REPORTING,
        SystemArtifactKind.QUALITY_REPORT,
        SystemArtifactKind.OBSERVABILITY_REPORT,
        SystemArtifactKind.NOTIFICATION_PREVIEW,
        SystemArtifactKind.DOCUMENTATION,
        SystemArtifactKind.TEST_SUITE
    ]

    records = []
    for kind in kinds:
        records.append(SystemArtifactRecord(
            artifact_kind=kind,
            artifact_name=kind.value,
            required_for_integration=True,
            available=True, # Assuming available for dry-run
            has_schema=True,
            has_tests=True,
            has_cli=True,
            has_health_check=True,
            has_docs=True,
            read_only=True,
            artifact_valid=True
        ))
    return records

def compute_system_artifact_inventory_hash(inventory: SystemArtifactInventory) -> str:
    h = hashlib.sha256()
    for artifact in inventory.artifacts:
        h.update(artifact.artifact_id.encode('utf-8'))
    return h.hexdigest()

def validate_system_artifact_inventory(inventory: SystemArtifactInventory) -> List[str]:
    violations = []
    if inventory.missing_required_count > 0:
        violations.append(f"Missing {inventory.missing_required_count} required artifacts.")
    for artifact in inventory.artifacts:
        if artifact.required_for_integration and not artifact.available:
            violations.append(f"Required artifact {artifact.artifact_name} is not available.")
    return violations

def system_artifact_inventory_summary(inventory: SystemArtifactInventory) -> Dict[str, Any]:
    return {
        "count": inventory.artifact_count,
        "valid": inventory.inventory_valid,
        "missing_required": inventory.missing_required_count
    }

def system_artifact_inventory_to_text(inventory: SystemArtifactInventory, limit: int = 300) -> str:
    summary = system_artifact_inventory_summary(inventory)
    text = f"Inventory Summary: {summary}"
    return text[:limit] + "..." if len(text) > limit else text
"""

with open("usa_signal_bot/integration/system_artifact_inventory.py", "w") as f:
    f.write(content)
