from typing import Any, Optional
from usa_signal_bot.provider_final_acceptance.phase115_models import (
    ProviderFreezeIngestionResult,
    DataProviderFinalAcceptanceReport,
    ProviderLayerClosureBundle,
    FeatureFactorEngineKickoffGate
)

def validate_final_no_execution_boundary(
    ingestion: Optional[ProviderFreezeIngestionResult] = None,
    acceptance: Optional[DataProviderFinalAcceptanceReport] = None,
    closure: Optional[ProviderLayerClosureBundle] = None,
    gate: Optional[FeatureFactorEngineKickoffGate] = None
) -> list[str]:
    errors = []

    if ingestion:
        if ingestion.activation_allowed:
            errors.append("activation_allowed is true in ingestion.")
        if ingestion.active_paper_enabled:
            errors.append("active_paper_enabled is true in ingestion.")
        if ingestion.broker_execution_enabled:
            errors.append("broker_execution_enabled is true in ingestion.")
        if ingestion.order_creation_enabled:
            errors.append("order_creation_enabled is true in ingestion.")
        if ingestion.paper_state_mutation_enabled:
            errors.append("paper_state_mutation_enabled is true in ingestion.")
        if ingestion.telegram_real_send_enabled:
            errors.append("telegram_real_send_enabled is true in ingestion.")
        if ingestion.scraping_enabled:
            errors.append("scraping_enabled is true in ingestion.")
        if ingestion.html_parse_enabled:
            errors.append("html_parse_enabled is true in ingestion.")
        if ingestion.paid_api_enabled:
            errors.append("paid_api_enabled is true in ingestion.")
        if ingestion.dashboard_enabled:
            errors.append("dashboard_enabled is true in ingestion.")
        if ingestion.network_default_enabled:
            errors.append("network_default_enabled is true in ingestion.")
        if ingestion.network_used:
            errors.append("network_used is true in ingestion.")
        if ingestion.paid_api_used:
            errors.append("paid_api_used is true in ingestion.")
        if ingestion.scraping_used:
            errors.append("scraping_used is true in ingestion.")
        if ingestion.html_parsing_used:
            errors.append("html_parsing_used is true in ingestion.")
        if ingestion.broker_used:
            errors.append("broker_used is true in ingestion.")
        if ingestion.order_created:
            errors.append("order_created is true in ingestion.")
        if ingestion.paper_state_mutated:
            errors.append("paper_state_mutated is true in ingestion.")
        if ingestion.telegram_real_sent:
            errors.append("telegram_real_sent is true in ingestion.")
        if ingestion.dashboard_started:
            errors.append("dashboard_started is true in ingestion.")
        if ingestion.produces_trade_signal:
            errors.append("produces_trade_signal is true in ingestion.")
        if ingestion.produces_order_decision:
            errors.append("produces_order_decision is true in ingestion.")

    if gate:
        if gate.activation_allowed:
            errors.append("activation_allowed is true in kickoff gate.")

    return errors

def final_no_execution_boundary_passed(errors: list[str]) -> bool:
    return len(errors) == 0

def final_no_execution_boundary_summary(errors: list[str]) -> dict[str, Any]:
    return {"passed": len(errors) == 0, "errors": errors}

def final_no_execution_boundary_to_text(errors: list[str]) -> str:
    if not errors:
        return "No-Execution Boundary: PASS"
    return f"No-Execution Boundary: FAIL ({len(errors)} errors)"
