
from typing import Any
from usa_signal_bot.data_providers.phase106_models import (
    ProviderAbstractionContext, ProviderKickoffGateIngestionResult,
    create_provider_abstraction_context_id, _now
)
from usa_signal_bot.core.enums import ProviderAbstractionStatus, ProviderAbstractionDecision
from usa_signal_bot.data_providers.provider_capability_matrix import build_provider_capability_matrix
from usa_signal_bot.data_providers.provider_safety_policy import build_provider_safety_policy

def build_provider_abstraction_context(kickoff: ProviderKickoffGateIngestionResult | None = None) -> ProviderAbstractionContext:
    if kickoff and not kickoff.ready_for_phase106:
        status = ProviderAbstractionStatus.BLOCKED
        decision = ProviderAbstractionDecision.BLOCK
    else:
        status = ProviderAbstractionStatus.CREATED
        decision = ProviderAbstractionDecision.CREATE_PROVIDER_ABSTRACTION

    return ProviderAbstractionContext(
        context_id=create_provider_abstraction_context_id(),
        created_at_utc=_now(),
        status=status,
        decision=decision,
        source_kickoff_gate_id=kickoff.source_gate_id if kickoff else None,
        kickoff_ingestion=kickoff,
        registry_entries=[],
        capability_matrix=build_provider_capability_matrix(),
        safety_policy=build_provider_safety_policy(),
        fallback_plans=[],
        provider_abstraction_ready=True,
        provider_skeletons_ready=True,
        provider_registry_valid=True,
        provider_safety_valid=True,
        metadata_only=True,
        activation_allowed=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        scraping_enabled=False,
        html_parse_enabled=False,
        dashboard_enabled=False,
        paid_api_enabled=False,
        provider_network_fetch_enabled_now=False,
        risk_flags=[],
        warnings=[],
        errors=[]
    )

def build_default_provider_abstraction_context() -> ProviderAbstractionContext:
    return build_provider_abstraction_context(None)

def provider_abstraction_context_summary(context: ProviderAbstractionContext) -> dict[str, Any]:
    return {"status": context.status}

def provider_abstraction_context_to_text(context: ProviderAbstractionContext, limit: int = 300) -> str:
    return f"Context {context.context_id}: {context.status}"
