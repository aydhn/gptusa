from typing import Any, Dict, List
from usa_signal_bot.provider_freeze.phase114_models import (
    DataLayerRehearsalScenario,
    create_rehearsal_scenario_id,
    _utcnow_str
)
from usa_signal_bot.core.enums import DataLayerRehearsalScenarioKind, ProviderFreezeRiskFlag

def build_rehearsal_scenario(kind: DataLayerRehearsalScenarioKind, name: str, description: str) -> DataLayerRehearsalScenario:
    return DataLayerRehearsalScenario(
        scenario_id=create_rehearsal_scenario_id(),
        created_at_utc=_utcnow_str(),
        scenario_kind=kind,
        name=name,
        description=description,
        required=True,
        metadata_only=True,
        dry_run_only=True,
        research_data_only=True,
        allow_network=False,
        allow_paid_api=False,
        allow_scraping=False,
        allow_html_parsing=False,
        allow_broker=False,
        allow_order=False,
        allow_paper_mutation=False,
        allow_telegram_real_send=False,
        allow_dashboard=False
    )

def build_default_rehearsal_scenarios() -> List[DataLayerRehearsalScenario]:
    return [
        build_rehearsal_scenario(DataLayerRehearsalScenarioKind.PROVIDER_REGISTRY_REHEARSAL, "Provider Registry Rehearsal", "Rehearses registry operations without network."),
        build_rehearsal_scenario(DataLayerRehearsalScenarioKind.CACHE_LOOKUP_REHEARSAL, "Cache Lookup Rehearsal", "Rehearses cache read operations."),
        build_rehearsal_scenario(DataLayerRehearsalScenarioKind.QUALITY_SCORING_REHEARSAL, "Quality Scoring Rehearsal", "Rehearses scoring without scraping."),
        build_rehearsal_scenario(DataLayerRehearsalScenarioKind.PROVIDER_ROUTE_REHEARSAL, "Provider Route Rehearsal", "Rehearses routing logic without execution."),
        build_rehearsal_scenario(DataLayerRehearsalScenarioKind.SOURCE_BLEND_REHEARSAL, "Source Blend Rehearsal", "Rehearses blending sources strictly offline."),
        build_rehearsal_scenario(DataLayerRehearsalScenarioKind.EVENT_CONTEXT_REHEARSAL, "Event Context Rehearsal", "Rehearses event context metadata creation."),
        build_rehearsal_scenario(DataLayerRehearsalScenarioKind.CALENDAR_VALIDATION_REHEARSAL, "Calendar Validation Rehearsal", "Rehearses calendar validation rules."),
        build_rehearsal_scenario(DataLayerRehearsalScenarioKind.LINEAGE_AUDIT_REHEARSAL, "Lineage Audit Rehearsal", "Rehearses lineage audit tracking."),
        build_rehearsal_scenario(DataLayerRehearsalScenarioKind.OUTPUT_CONTRACT_REHEARSAL, "Output Contract Rehearsal", "Rehearses output contract restrictions."),
        build_rehearsal_scenario(DataLayerRehearsalScenarioKind.NO_EXECUTION_REHEARSAL, "No Execution Rehearsal", "Rehearses strict no-execution safeguards.")
    ]

def validate_rehearsal_scenario_safety(scenario: DataLayerRehearsalScenario) -> List[str]:
    errors = []
    if not scenario.metadata_only:
        errors.append("Scenario must be metadata_only.")
    if not scenario.dry_run_only:
        errors.append("Scenario must be dry_run_only.")
    if not scenario.research_data_only:
        errors.append("Scenario must be research_data_only.")

    for flag in [
        "allow_network", "allow_paid_api", "allow_scraping", "allow_html_parsing",
        "allow_broker", "allow_order", "allow_paper_mutation", "allow_telegram_real_send",
        "allow_dashboard"
    ]:
        if getattr(scenario, flag):
            errors.append(f"Scenario must not allow {flag}.")

    return errors

def rehearsal_scenario_summary(scenarios: List[DataLayerRehearsalScenario]) -> Dict[str, Any]:
    return {
        "total": len(scenarios),
        "unsafe": sum(1 for s in scenarios if len(validate_rehearsal_scenario_safety(s)) > 0)
    }

def rehearsal_scenarios_to_text(scenarios: List[DataLayerRehearsalScenario], limit: int = 200) -> str:
    lines = [f"Rehearsal Scenarios ({len(scenarios)}):"]
    for s in scenarios[:limit]:
        lines.append(f"  - {s.name} ({s.scenario_kind.value})")
    return "\n".join(lines)
