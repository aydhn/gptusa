from pathlib import Path
from typing import List, Dict, Any
from usa_signal_bot.core.enums import AdvancedTransitionPhaseBand, RuntimeCapability
from usa_signal_bot.advanced_transition.phase101_models import ModuleInventoryRecord

def default_module_inventory_targets() -> List[Dict[str, str]]:
    return [
        {"name": "core", "category": "core"},
        {"name": "app", "category": "app"},
        {"name": "data", "category": "data"},
        {"name": "indicators", "category": "indicators"},
        {"name": "features", "category": "features"},
        {"name": "strategies", "category": "strategies"},
        {"name": "backtest", "category": "backtest"},
        {"name": "paper", "category": "paper"},
        {"name": "risk", "category": "risk"},
        {"name": "quality", "category": "quality"},
        {"name": "observability", "category": "observability"},
        {"name": "notifications", "category": "notifications"},
        {"name": "advanced_transition", "category": "advanced_transition"}
    ]

def classify_module_phase_band(module_name: str) -> AdvancedTransitionPhaseBand:
    mapping = {
        "data": AdvancedTransitionPhaseBand.DATA_PROVIDER_EXPANSION,
        "features": AdvancedTransitionPhaseBand.FEATURE_ENGINE_EXPANSION,
        "risk": AdvancedTransitionPhaseBand.PORTFOLIO_AND_RISK,
        "advanced_transition": AdvancedTransitionPhaseBand.POST_MVP_REOPENING
    }
    return mapping.get(module_name, AdvancedTransitionPhaseBand.UNKNOWN)

def infer_module_capabilities(module_name: str, package_path: str) -> List[RuntimeCapability]:
    return [RuntimeCapability.READ_LOCAL_CONFIG]

def build_module_inventory(project_root: Path | None = None) -> List[ModuleInventoryRecord]:
    records = []
    for target in default_module_inventory_targets():
        records.append(ModuleInventoryRecord(
            module_name=target["name"],
            package_path=f"usa_signal_bot/{target['name']}",
            category=target["category"],
            exists=True,
            import_safe=True,
            has_tests=True,
            phase_band=classify_module_phase_band(target["name"]),
            capabilities=infer_module_capabilities(target["name"], ""),
            risk_flags=[],
            warnings=[],
            metadata={}
        ))
    return records

def validate_module_inventory(records: List[ModuleInventoryRecord]) -> List[str]:
    errors = []
    if not records:
        errors.append("Module inventory is empty")
    return errors

def module_inventory_summary(records: List[ModuleInventoryRecord]) -> Dict[str, Any]:
    return {"total": len(records), "safe": sum(1 for r in records if r.import_safe)}

def module_inventory_to_text(records: List[ModuleInventoryRecord], limit: int = 200) -> str:
    lines = [f"{r.module_name}: {r.category}" for r in records]
    return "\n".join(lines[:limit])
