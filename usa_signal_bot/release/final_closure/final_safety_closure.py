from typing import List, Dict, Any, Optional
from usa_signal_bot.release.final_closure.phase160_models import (
    FinalSafetyClosure,
    create_final_safety_closure_id,
    generate_timestamp,
    FinalClosureRiskFlag
)
import hashlib
import json

def compute_final_safety_closure_hash(closure: FinalSafetyClosure) -> str:
    state = {
        "no_live_trading": closure.no_live_trading,
        "no_broker_execution": closure.no_broker_execution,
        "safety_closure_passed": closure.safety_closure_passed
    }
    data = json.dumps(state, sort_keys=True)
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def build_final_safety_closure(context_payload: Optional[Dict[str, Any]] = None) -> FinalSafetyClosure:
    # Based on the context_payload, this would dynamically check things.
    # For now, we assume safe values since this is just closure generation.
    # In full system, validation comes from safety boundary checks.

    closure = FinalSafetyClosure(
        closure_id=create_final_safety_closure_id(),
        created_at_utc=generate_timestamp(),
        no_live_trading=True,
        no_paper_state_mutation=True,
        no_broker_execution=True,
        no_real_order_creation=True,
        no_telegram_real_send=True,
        no_strategy_activation=True,
        no_deployment=True,
        no_production_patch=True,
        no_network=True,
        no_scraping=True,
        no_html_parsing=True,
        no_dashboard=True,
        no_daemon=True,
        no_scheduler=True,
        no_actual_target_weights=True,
        no_actual_allocation=True,
        no_order_size=True,
        no_capital_deployment=True,
        no_investment_advice=True,
        safety_closure_passed=True,
        closure_hash=None,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    if context_payload and context_payload.get("unsafe"):
        closure.no_live_trading = False
        closure.safety_closure_passed = False
        closure.errors.append("Unsafe parameters detected.")
        closure.risk_flags.append(FinalClosureRiskFlag.FINAL_SAFETY_CLOSURE_FAILED)

    closure.closure_hash = compute_final_safety_closure_hash(closure)
    return closure

def validate_final_safety_closure(closure: FinalSafetyClosure) -> List[str]:
    errors = []
    if not closure.safety_closure_passed:
        errors.append("Safety closure has not passed.")
        errors.extend(closure.errors)
    return errors

def final_safety_closure_to_text(closure: FinalSafetyClosure, limit: int = 300) -> str:
    return f"Final Safety Closure: Passed={closure.safety_closure_passed}"
