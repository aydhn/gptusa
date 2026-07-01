import json
import logging
from typing import Any, Dict, List

from usa_signal_bot.integration.phase158_models import (
    IntegrationInputReference,
    IntegrationInputKind,
)
from usa_signal_bot.core.enums import FullSystemIntegrationRiskFlag

logger = logging.getLogger(__name__)

FORBIDDEN_FIELDS = [
    "broker_order",
    "paper_order",
    "live_order",
    "sent_to_broker",
    "strategy_active",
    "deployment_enabled",
    "production_patch",
    "live_signal",
    "buy_signal",
    "sell_signal",
    "target_weight",
    "portfolio_weight",
    "actual_target_weight",
    "allocation",
    "actual_allocation",
    "capital_allocation",
    "position_size",
    "order_size",
    "real_order",
    "telegram_sent",
]


def build_integration_input_references(
    payloads: Dict[str, Any],
) -> List[IntegrationInputReference]:
    references = []
    for key, value in payloads.items():
        ref = IntegrationInputReference(
            input_kind=IntegrationInputKind.UNKNOWN,
            source_artifact_name=key,
            available=True,
            read_only=True,
            valid=True,
            research_data_only=True,
            integration_only=True,
        )

        forbidden = detect_forbidden_integration_fields(value)
        if forbidden:
            ref.valid = False
            ref.forbidden_fields_detected = forbidden
            ref.risk_flags.append(
                FullSystemIntegrationRiskFlag.FORBIDDEN_INTEGRATION_FIELD
            )

        references.append(ref)
    return references


def detect_forbidden_integration_fields(payload: Dict[str, Any]) -> List[str]:
    detected = []
    try:
        payload_str = json.dumps(payload).lower()
        for field in FORBIDDEN_FIELDS:
            if field.lower() in payload_str:
                detected.append(field)
    except Exception as e:
        logger.warning(
            "Failed to serialize payload for forbidden field detection: %s", e
        )
    return detected


def detect_forbidden_integration_columns(columns: List[str]) -> List[str]:
    detected = []
    for col in columns:
        for forbidden in FORBIDDEN_FIELDS:
            if forbidden.lower() in col.lower():
                detected.append(col)
    return detected


def validate_integration_input_references(
    items: List[IntegrationInputReference],
) -> List[str]:
    violations = []
    for item in items:
        if not item.valid:
            violations.append(
                f"Invalid reference {item.source_artifact_name}: forbidden fields {item.forbidden_fields_detected}"
            )
    return violations


def integration_input_resolver_summary(
    items: List[IntegrationInputReference],
) -> Dict[str, Any]:
    return {
        "total_references": len(items),
        "valid_references": sum(1 for i in items if i.valid),
        "invalid_references": sum(1 for i in items if not i.valid),
    }


def integration_input_resolver_to_text(
    items: List[IntegrationInputReference], limit: int = 300
) -> str:
    summary = integration_input_resolver_summary(items)
    text = f"Input Resolver: {summary}"
    return text[:limit] + "..." if len(text) > limit else text
