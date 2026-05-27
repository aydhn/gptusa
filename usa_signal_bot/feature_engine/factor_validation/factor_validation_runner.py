import pandas as pd
from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.feature_engine.factor_validation.phase122_models import (
    FactorValidationResult,
    FactorValidationRule,
    FactorValidationQuality,
    FactorValidationRuleStatus,
    create_factor_validation_result_id,
    validate_factor_validation_result
)
from usa_signal_bot.feature_engine.factor_validation.factor_validation_rules import build_factor_validation_rules_for_table

def factor_validation_result_quality(rules: list[FactorValidationRule]) -> FactorValidationQuality:
    if any(r.status == FactorValidationRuleStatus.FAIL for r in rules):
        return FactorValidationQuality.INVALID
    if any(r.status == FactorValidationRuleStatus.WARNING for r in rules):
        return FactorValidationQuality.WARNING
    return FactorValidationQuality.HIGH

def factor_validation_passed(result: FactorValidationResult) -> bool:
    return result.validation_passed

def run_factor_validation_for_table(symbol: str, df: pd.DataFrame, factor_table_path: str | None = None) -> FactorValidationResult:
    rules = build_factor_validation_rules_for_table(symbol, df)

    passed_rules = sum(1 for r in rules if r.status == FactorValidationRuleStatus.PASS)
    warning_rules = sum(1 for r in rules if r.status == FactorValidationRuleStatus.WARNING)
    failed_rules = sum(1 for r in rules if r.status == FactorValidationRuleStatus.FAIL)
    blocked_rules = sum(1 for r in rules if r.status == FactorValidationRuleStatus.BLOCKED)

    validation_passed = failed_rules == 0 and blocked_rules == 0

    factor_cols = [c for c in df.columns if c not in ['symbol', 'timestamp', 'date', 'datetime']]

    forbidden_columns = []
    for r in rules:
        if r.rule_kind.name == "FORBIDDEN_COLUMNS_ABSENT" and r.status == FactorValidationRuleStatus.FAIL:
            # Not exact but proxy
            forbidden_columns = ["detected"]

    res = FactorValidationResult(
        validation_id=create_factor_validation_result_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        symbol=symbol,
        factor_table_path=factor_table_path,
        rules=rules,
        total_rules=len(rules),
        passed_rules=passed_rules,
        warning_rules=warning_rules,
        failed_rules=failed_rules,
        blocked_rules=blocked_rules,
        validation_passed=validation_passed,
        quality=factor_validation_result_quality(rules),
        factor_columns=factor_cols,
        forbidden_columns_present=forbidden_columns,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    validate_factor_validation_result(res)
    return res

def run_factor_validation_for_tables(tables: dict[str, pd.DataFrame]) -> list[FactorValidationResult]:
    return [run_factor_validation_for_table(sym, df) for sym, df in tables.items()]

def factor_validation_runner_summary(results: list[FactorValidationResult]) -> dict[str, Any]:
    passed = sum(1 for r in results if r.validation_passed)
    return {"total": len(results), "passed": passed}

def factor_validation_runner_to_text(results: list[FactorValidationResult], limit: int = 200) -> str:
    return f"Validated {len(results)} tables."
