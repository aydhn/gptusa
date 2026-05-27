from typing import Any
from usa_signal_bot.feature_engine.factor_validation.phase122_models import (
    FactorValidationContext,
    FactorValidationResult,
    FactorDriftReport,
    FactorVersionMetadata,
    FactorArtifactManifest,
    FactorStoreHardeningResult,
    FactorValidationRiskFlag
)

def factor_persistence_text_has_trade_or_execution_language(text: str) -> bool:
    t = text.lower()
    bad = [
        'buy', 'sell', 'entry', 'exit', 'order', 'broker', 'position',
        'portfolio_weight', 'target_weight', 'allocation', 'demo_order',
        'live_order', 'sent_to_broker'
    ]
    for b in bad:
        # whitelist macd_signal_9
        if b == 'signal' and 'macd_signal' in t:
            continue
        if b in t and b != 'signal':
            return True
        if b == 'signal' and 'buy_signal' in t or 'sell_signal' in t:
            return True
    return False

def validate_factor_persistence_columns_safety(columns: list[str]) -> list[str]:
    err = []
    for c in columns:
        if factor_persistence_text_has_trade_or_execution_language(c):
            err.append(f"Forbidden column detected: {c}")
    return err

def validate_factor_validation_context_safety(context: FactorValidationContext) -> list[str]:
    err = []
    if context.activation_allowed or context.strategy_activation_allowed or context.active_paper_enabled:
        err.append("Context allows activation")
    if context.broker_execution_enabled or context.order_creation_enabled or context.paper_state_mutation_enabled:
        err.append("Context allows execution")
    return err

def validate_factor_validation_results_safety(results: list[FactorValidationResult]) -> list[str]:
    err = []
    for r in results:
        if len(r.forbidden_columns_present) > 0:
            err.append(f"Forbidden columns in result {r.validation_id}")
    return err

def validate_factor_drift_reports_safety(reports: list[FactorDriftReport]) -> list[str]:
    err = []
    for r in reports:
        if r.produces_trade_signal or r.produces_order_decision or r.produces_portfolio_weights:
            err.append("Drift report produced signal")
    return err

def validate_factor_versioning_safety(metadata: FactorVersionMetadata) -> list[str]:
    err = []
    if metadata.activation_allowed or metadata.strategy_activation_allowed:
        err.append("Version enables activation")
    return err

def validate_factor_manifest_safety(manifest: FactorArtifactManifest) -> list[str]:
    err = []
    if manifest.secret_violation_count > 0:
        err.append("Secret violation in manifest")
    if manifest.execution_language_violation_count > 0:
        err.append("Execution language in manifest")
    return err

def validate_factor_store_hardening_safety(result: FactorStoreHardeningResult) -> list[str]:
    err = []
    if not result.no_secret_leak or not result.no_forbidden_columns or not result.no_execution_language:
        err.append("Store hardening failed safety")
    return err

def collect_factor_validation_risk_flags(context: FactorValidationContext | None = None) -> list[FactorValidationRiskFlag]:
    return []

def factor_persistence_safety_summary(errors: list[str]) -> dict[str, Any]:
    return {"errors_count": len(errors)}

def factor_persistence_safety_to_text(errors: list[str]) -> str:
    return "Safety checked." if not errors else f"{len(errors)} safety errors found."
