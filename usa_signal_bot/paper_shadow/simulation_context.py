from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowSimulationContext,
    ShadowRuntimeMode,
    create_shadow_context_id
)
from usa_signal_bot.core.exceptions import ShadowSimulationContextError

def build_shadow_simulation_context_from_sandbox_payload(
    payload: dict[str, Any],
    starting_equity_usd: float = 100000.0,
    runtime_mode: ShadowRuntimeMode = ShadowRuntimeMode.FULL_PAPER_SHADOW
) -> ShadowSimulationContext:
    from usa_signal_bot.paper_shadow.sandbox_ingestion import extract_sandbox_bundle_refs
    refs = extract_sandbox_bundle_refs(payload)

    context = ShadowSimulationContext(
        context_id=create_shadow_context_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        runtime_mode=runtime_mode,
        starting_equity_usd=starting_equity_usd,
        in_memory_config=payload.get("config", {}),
        allow_real_orders=False,
        allow_broker_calls=False,
        allow_paper_state_mutation=False,
        allow_telegram_real_send=False,
        allow_production_config_write=False,
        warnings=[],
        errors=[],
        source_sandbox_id=refs.get("source_sandbox_id"),
        source_bundle_id=refs.get("source_bundle_id"),
        source_bundle_version=refs.get("source_bundle_version"),
        isolated_output_path="data/paper_shadow/outputs/isolated",
    )
    return context

def build_mock_shadow_simulation_context(starting_equity_usd: float = 100000.0) -> ShadowSimulationContext:
    return ShadowSimulationContext(
        context_id=create_shadow_context_id("mock_shadow_context"),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        runtime_mode=ShadowRuntimeMode.MOCK_SHADOW,
        starting_equity_usd=starting_equity_usd,
        in_memory_config={"mock": True},
        allow_real_orders=False,
        allow_broker_calls=False,
        allow_paper_state_mutation=False,
        allow_telegram_real_send=False,
        allow_production_config_write=False,
        warnings=[],
        errors=[],
        isolated_output_path="data/paper_shadow/outputs/mock",
    )

def validate_shadow_context_safety(context: ShadowSimulationContext) -> list[str]:
    errors = []
    if context.allow_real_orders:
        errors.append("Context allows real orders")
    if context.allow_broker_calls:
        errors.append("Context allows broker calls")
    if context.allow_paper_state_mutation:
        errors.append("Context allows paper state mutation")
    if context.allow_telegram_real_send:
        errors.append("Context allows telegram real send")
    if context.allow_production_config_write:
        errors.append("Context allows production config write")
    return errors

def shadow_context_summary(context: ShadowSimulationContext) -> dict[str, Any]:
    return {
        "context_id": context.context_id,
        "runtime_mode": context.runtime_mode.value,
        "starting_equity_usd": context.starting_equity_usd,
        "is_safe": not validate_shadow_context_safety(context)
    }

def shadow_context_to_text(context: ShadowSimulationContext) -> str:
    summary = shadow_context_summary(context)
    text = "Shadow Simulation Context\n"
    text += f"ID: {summary['context_id']}\n"
    text += f"Mode: {summary['runtime_mode']}\n"
    text += f"Starting Equity: ${summary['starting_equity_usd']}\n"
    text += f"Is Safe: {summary['is_safe']}\n"
    return text
