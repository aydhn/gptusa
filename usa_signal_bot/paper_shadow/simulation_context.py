from typing import Any, Dict, List
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowSimulationContext, create_shadow_context_id, get_utc_now_str
)
from usa_signal_bot.core.enums import ShadowRuntimeMode

def build_shadow_simulation_context_from_sandbox_payload(
    payload: Dict[str, Any],
    starting_equity_usd: float = 100000.0,
    runtime_mode: ShadowRuntimeMode = ShadowRuntimeMode.FULL_PAPER_SHADOW
) -> ShadowSimulationContext:

    return ShadowSimulationContext(
        context_id=create_shadow_context_id(),
        created_at_utc=get_utc_now_str(),
        source_sandbox_id=payload.get("sandbox_id"),
        source_bundle_id=payload.get("bundle_id"),
        source_bundle_version=payload.get("bundle_version"),
        runtime_mode=runtime_mode,
        starting_equity_usd=starting_equity_usd,
        in_memory_config=payload.get("config", {}),
        isolated_output_path=payload.get("isolated_output_path"),
        allow_real_orders=False,
        allow_broker_calls=False,
        allow_paper_state_mutation=False,
        allow_telegram_real_send=False,
        allow_production_config_write=False,
        warnings=[],
        errors=[]
    )

def build_mock_shadow_simulation_context(starting_equity_usd: float = 100000.0) -> ShadowSimulationContext:
    return ShadowSimulationContext(
        context_id=create_shadow_context_id("mock_context"),
        created_at_utc=get_utc_now_str(),
        source_sandbox_id=None,
        source_bundle_id=None,
        source_bundle_version=None,
        runtime_mode=ShadowRuntimeMode.MOCK_SHADOW,
        starting_equity_usd=starting_equity_usd,
        in_memory_config={"mock": True},
        isolated_output_path="/tmp/mock_shadow_output",
        allow_real_orders=False,
        allow_broker_calls=False,
        allow_paper_state_mutation=False,
        allow_telegram_real_send=False,
        allow_production_config_write=False,
        warnings=[],
        errors=[]
    )

def validate_shadow_context_safety(context: ShadowSimulationContext) -> List[str]:
    errors = []
    if context.allow_real_orders:
        errors.append("Shadow context must not allow real orders.")
    if context.allow_broker_calls:
        errors.append("Shadow context must not allow broker calls.")
    if context.allow_paper_state_mutation:
        errors.append("Shadow context must not allow paper state mutation.")
    if context.allow_telegram_real_send:
        errors.append("Shadow context must not allow real telegram sends.")
    if context.allow_production_config_write:
        errors.append("Shadow context must not allow production config writes.")
    return errors

def shadow_context_summary(context: ShadowSimulationContext) -> Dict[str, Any]:
    return {
        "context_id": context.context_id,
        "runtime_mode": context.runtime_mode.value,
        "starting_equity_usd": context.starting_equity_usd,
        "is_safe": len(validate_shadow_context_safety(context)) == 0
    }

def shadow_context_to_text(context: ShadowSimulationContext) -> str:
    return f"ShadowContext({context.context_id}, mode={context.runtime_mode.value}, eq={context.starting_equity_usd})"
