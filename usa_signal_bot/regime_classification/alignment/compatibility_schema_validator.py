from typing import Any
from usa_signal_bot.regime_classification.alignment.phase131_models import (
    RegimeContextCompatibilityResult, MarketBehaviorOverlayResult, RegimeAlignmentContext
)

FORBIDDEN_FRAGMENTS = [
    "buy", "sell", "entry", "exit", "order", "broker", "position",
    "portfolio_weight", "target_weight", "allocation", "paper", "live",
    "demo_order", "live_order", "sent_to_broker", "deploy", "production_patch"
]

def validate_compatibility_result_schema(result: RegimeContextCompatibilityResult) -> list[str]:
    return validate_no_forbidden_alignment_columns([result.source_column])

def validate_overlay_result_schema(result: MarketBehaviorOverlayResult) -> list[str]:
    return validate_no_forbidden_alignment_columns([result.target_column] if result.target_column else [])

def validate_alignment_context_schema(context: RegimeAlignmentContext) -> list[str]:
    errs = []
    for o in context.overlay_results:
        errs.extend(validate_overlay_result_schema(o))
    for c in context.compatibility_results:
        errs.extend(validate_compatibility_result_schema(c))
    return errs

def validate_alignment_column_names(columns: list[str]) -> list[str]:
    return validate_no_forbidden_alignment_columns(columns)

def validate_no_forbidden_alignment_columns(columns: list[str]) -> list[str]:
    errs = []
    for c in columns:
        cl = c.lower()
        for f in FORBIDDEN_FRAGMENTS:
            if f in cl and cl != "macd_signal_9":
                if f == "signal" and cl == "macd_signal_9": continue
                if f != "signal":
                    errs.append(f"Forbidden column name {c} containing {f}")
    return errs

def compatibility_schema_summary(errors: list[str]) -> dict[str, Any]:
    return {"error_count": len(errors)}

def compatibility_schema_to_text(errors: list[str]) -> str:
    if not errors: return "Schema OK"
    return f"Schema ERRORS: {', '.join(errors)}"
