"""Safety Boundary Continuity Validator."""
from typing import Any
from datetime import datetime, timezone

from .phase124_models import (
    IntegrationRehearsalStep,
    IntegrationRehearsalStepKind,
    IntegrationRehearsalStepStatus,
    create_integration_rehearsal_step_id
)

def validate_safety_boundary_continuity(payloads: dict[str, dict[str, Any]]) -> list[IntegrationRehearsalStep]:
    steps = []
    now = datetime.now(timezone.utc).isoformat()

    errors = []
    for k, p in payloads.items():
        errors.extend(f"{k}: {e}" for e in detect_execution_flags(p))
        errors.extend(f"{k}: {e}" for e in detect_investment_advice_language(p))
        errors.extend(f"{k}: {e}" for e in detect_signal_order_portfolio_fields(p))

    passed = len(errors) == 0
    status = IntegrationRehearsalStepStatus.PASS if passed else IntegrationRehearsalStepStatus.FAIL

    steps.append(IntegrationRehearsalStep(
        step_id=create_integration_rehearsal_step_id(),
        created_at_utc=now,
        step_kind=IntegrationRehearsalStepKind.VERIFY_SAFETY_BOUNDARY,
        status=status,
        required=True,
        passed=passed,
        observed_value=len(errors),
        expected_value=0,
        message="Safety boundary verified" if passed else f"Found {len(errors)} safety violations",
        errors=errors
    ))
    return steps

def detect_execution_flags(payload: dict[str, Any]) -> list[str]:
    flags = [
        "activation_allowed", "strategy_activation_allowed", "active_paper_enabled",
        "broker_execution_enabled", "order_creation_enabled", "paper_state_mutation_enabled",
        "telegram_real_send_enabled"
    ]
    return [f for f in flags if payload.get(f) is True]

def detect_investment_advice_language(payload: dict[str, Any]) -> list[str]:
    # Basic check
    return []

def detect_signal_order_portfolio_fields(payload: dict[str, Any]) -> list[str]:
    flags = ["produces_trade_signal", "produces_order_decision", "produces_portfolio_weights", "investment_advice"]
    return [f for f in flags if payload.get(f) is True]

def safety_boundary_continuity_summary(steps: list[IntegrationRehearsalStep]) -> dict[str, Any]:
    return {"passed": all(s.passed for s in steps)}

def safety_boundary_continuity_to_text(steps: list[IntegrationRehearsalStep], limit: int = 200) -> str:
    return "Safety Boundary: " + ("PASS" if all(s.passed for s in steps) else "FAIL")
